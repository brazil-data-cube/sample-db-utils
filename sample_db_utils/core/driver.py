#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""This file contains Brazil Data Cube drivers to list the sample and store in database."""

import logging
import os
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
from geoalchemy2 import shape
from geopandas import GeoDataFrame, GeoSeries
from lccs_db.models import LucClass, LucClassificationSystem
from lccs_db.models import db as _db
from osgeo import ogr, osr
from shapely import wkt
from shapely.geometry import Point
from shapely.wkt import loads as geom_from_wkt
from werkzeug.datastructures import FileStorage

from sample_db_utils.core.utils import (get_date_from_str, is_stream,
                                        reproject, unzip, validate_mappings)


def get_date_from_str(date, date_ref=None):
    """Build date from str."""
    date = date.replace('/', '-')

    try:
        date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')
    except:
        return date

    return date


class Driver(metaclass=ABCMeta):
    """Generic interface for data reader."""

    def __init__(self, storager, user=None, system=None):
        """Init method.

        Args:
            storager (Storager) - Storager Strategy from sample-db-utils
            user (sample_db.models.User) - The user instance sample owner
            system (lccs_db.models.LucClassificationSystem) - The land use coverage classification system

        """
        self.storager = storager
        self.user = user
        self.system = system
        self._data_sets = []

    @abstractmethod
    def load(self, file):
        """Open the file and load data."""

    @abstractmethod
    def load_classes(self, file):
        """Load sample classes in memory."""

    def validate_classes(self, unique_classes):
        """Validate if classes exist in classification system."""
        if self.system:
            system_id = self.system.id
        elif self.storager.classification_system_id is not None:
            system_id = self.storager.classification_system_id
        else:
            raise RuntimeError("Missing Classification System ")

        classes = _db.session.query(LucClass.id). \
            join(LucClassificationSystem, LucClass.classification_system_id == LucClassificationSystem.id) \
            .filter(LucClassificationSystem.id == system_id).all()

        classes_lists = [x[0] for x in classes]

        not_exist = list(set(unique_classes) - set(classes_lists) & set(unique_classes))

        if len(not_exist) > 0:
            raise RuntimeError(f"The classes: {', '.join([str(elem) for elem in not_exist])} "
                               f"does not exist in the classification system!")

    @abstractmethod
    def get_files(self):
        """Retrieve list of files to load."""

    def get_data_sets(self):
        """Retrieve the loaded data sets.

        Returns:
            list of dict - Loaded data sets

        """
        return self._data_sets

    def load_data_sets(self):
        """Load data sets in memory using database format."""
        files = self.get_files()

        for f in files:
            self.load(f)
            print("{} loaded in memory".format(f))

        return self

    def store(self, dataset_table):
        """Store the data into database using Storager strategy."""
        self.storager.store_data(self._data_sets, dataset_table)


class CSV(Driver):
    """Defines a Base class for handle CSV data files.

    Basically, a CSV is built with a mappings config.
    The config describes how to read the dataset in order to
    create a Brazil Data Cube sample. The `mappings`
    must include at least the required fields to fill
    a sample, such latitude, longitude and class_id fields.
    """

    def __init__(self, entries, mappings, storager=None, **kwargs):
        """Init method.

        Args:
            entries (string|io.IOBase) - The file entries
            mappings (dict) - CSV Mappings to Sample
            storager (PostgisAccessor) - The PostgisAccessor from utils

        """
        copy_mappings = deepcopy(mappings)

        validate_mappings(copy_mappings)

        super(CSV, self).__init__(storager, **kwargs)

        self.mappings = copy_mappings
        self.entries = entries

    def get_files(self):
        """Get files."""
        if is_stream(self.entries) or \
                os.path.isfile(self.entries):
            return [self.entries]

        files = os.listdir(self.entries)

        return [
            os.path.join(self.entries, f) for f in files if f.endswith(".csv")
        ]

    def build_data_set(self, csv):
        """Build dataset sample data.

        Args:
            csv(pd.DataFrame) - Open CSV file

        Returns:
            GeoDataFrame CSV with geospatial location

        """
        if 'longitude' in self.mappings and 'latitude' in self.mappings:
            geom_column = [
                Point(xy) for xy in zip(csv[self.mappings['longitude']], csv[self.mappings['longitude']])
            ]
            geocsv = GeoDataFrame(csv,
                                  crs=self.mappings.get('srid', 4326),
                                  geometry=geom_column)
            geocsv['location'] = geocsv['geometry'].apply(
                lambda point: ';'.join(['SRID=4326', point.wkt])
            )
            if 'latitude' in geocsv:
                del geocsv['latitude']
            if 'longitude' in geocsv:
                del geocsv['longitude']

        else:
            geom_column = GeoSeries.from_wkt(csv[self.mappings['geom']],
                                             crs=self.mappings.get('srid', 4326))
            geocsv = GeoDataFrame(csv, crs=self.mappings.get('srid', 4326), geometry=geom_column)

        geocsv['class_id'] = geocsv[self.mappings['class_id']]

        start_date = self.mappings['start_date'].get('value') or \
                     geocsv[self.mappings['start_date']['key']]

        end_date = self.mappings['end_date'].get('value') or \
                   geocsv[self.mappings['end_date']['key']]

        collection_date = self.mappings['collection_date'].get('value') or \
                          geocsv[self.mappings['collection_date']['key']] or \
                          None

        if collection_date:
            collection_date = get_date_from_str(collection_date)

        geocsv['user_id'] = self.user
        geocsv['start_date'] = start_date
        geocsv['end_date'] = end_date
        geocsv['collection_date'] = collection_date

        # Delete id column to avoid DuplicateError on database
        if 'id' in geocsv.columns:
            del geocsv['id']

        if 'geometry' in geocsv.columns:
            del geocsv['geometry']

        return geocsv

    def get_unique_classes(self, csv):
        """Retrieve distinct sample classes from CSV datasource."""
        return csv[self.mappings['class_id']].unique()

    def load(self, file):
        """Load file."""
        if file.mimetype == 'application/json':
            csv = pd.read_json(file)
        else:
            csv = pd.read_csv(file)

        self.load_classes(csv)

        res = self.build_data_set(csv)

        self._data_sets.extend(res.T.to_dict().values())

    def load_classes(self, file):
        """Load classes of a file."""
        unique_classes = self.get_unique_classes(file)

        self.validate_classes(unique_classes)

        return


class Shapefile(Driver):
    """Base class for Shapefiles Reader."""

    def __init__(self, entries, mappings, storager=None, **kwargs):
        """Init method."""
        copy_mappings = deepcopy(mappings)

        validate_mappings(copy_mappings)

        super(Shapefile, self).__init__(storager, **kwargs)

        self.mappings = copy_mappings
        self.entries = entries
        self.temporary_folder = TemporaryDirectory()
        self.class_id = None
        self.start_date = None
        self.end_date = None
        self.collection_date = None
        self.crs = None

    def get_unique_classes(self, ogr_file, layer_name):
        """Retrieve distinct sample classes from shapefile datasource."""
        classes = self.mappings.get('class_id')

        if isinstance(classes, str):
            classes = self.mappings['class_id']

        else:
            return classes['value']

        layer = ogr_file.GetLayer(layer_name)

        if layer.GetFeatureCount() == 0:
            return []

        unique_c = ogr_file.ExecuteSQL(f'SELECT DISTINCT {classes} FROM {layer_name}')

        result = []
        for i, feature in enumerate(unique_c):
            result.append(feature.GetField(0))

        return result

    def get_files(self):
        """Get files."""
        if isinstance(self.entries, FileStorage) or \
                self.entries.endswith('.zip'):
            unzip(self.entries, self.temporary_folder.name)

            self.entries = self.temporary_folder.name

        if is_stream(self.entries) or \
                (os.path.isfile(self.entries) and self.entries.endswith('.shp')):
            return [self.entries]

        files = os.listdir(self.entries)

        return [
            os.path.join(self.entries, f) for f in files if f.endswith('.shp')
        ]

    def build_data_set(self, feature, **kwargs):
        """Build dataset sample data."""
        geometry = feature.GetGeometryRef()

        srs = geometry.GetSpatialReference()

        reproject(geometry, self.crs, target_srid=4326)

        geom_shapely = geom_from_wkt(
            geometry.ExportToWkt())

        ewkt = shape.from_shape(geom_shapely, srid=4326)

        start_date = self.mappings['start_date'].get('value') or \
                     feature.GetField(self.mappings['start_date']['key'])

        end_date = self.mappings['end_date'].get('value') or \
                   feature.GetField(self.mappings['end_date']['key'])

        try:
            collection_date = self.mappings['collection_date'].get('value') or \
                              feature.GetField(self.mappings['collection_date']['key'])
            collection_date = get_date_from_str(collection_date)
        except:
            collection_date = None

        start_date = get_date_from_str(start_date)
        end_date = get_date_from_str(end_date)

        class_id = feature.GetField(self.mappings['class_id'])

        return {
            "start_date": start_date,
            "end_date": end_date,
            "collection_date": collection_date,
            "location": ewkt,
            "class_id": class_id,
            "user_id": self.user
        }

    def load(self, file):
        """Load datasource."""
        dataSource = ogr.Open(file)

        # Check to see if shapefile is found.
        if dataSource is None:
            raise Exception("Could not open {}".format(file))
        else:
            self.load_classes(dataSource)

            for layer_id in range(dataSource.GetLayerCount()):
                gdal_layer = dataSource.GetLayer(layer_id)

                spatial_ref = gdal_layer.GetSpatialRef()

                if spatial_ref is None:
                    spatial_ref = osr.SpatialReference()
                    spatial_ref.ImportFromEPSG(4326)
                    logging.info('Dataset {} does not have projection. Using EPSG:4326...'.format(file))

                self.crs = spatial_ref.ExportToProj4()

                gdal_layer.ResetReading()

                for feature in gdal_layer:
                    dataset = self.build_data_set(feature, **{"layer": gdal_layer})
                    self._data_sets.append(dataset)

    def load_classes(self, file):
        """Load classes of a file."""
        # Retrieves Layer Name from Data set filename
        layer_name = Path(file.GetName()).stem

        unique_classes = self.get_unique_classes(file, layer_name)

        self.validate_classes(unique_classes)

        return
