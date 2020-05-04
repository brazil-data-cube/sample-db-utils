#
# This file is part of Sample Database Utils.
# Copyright (C) 2019 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""This file contains Brazil Data Cube drivers to list the sample and store in database."""

import logging
import os
from abc import abstractmethod, ABCMeta
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from osgeo import ogr, osr
import pandas as pd
from geoalchemy2 import shape
from geopandas import GeoDataFrame
from shapely.geometry import Point
from shapely.wkt import loads as geom_from_wkt
from werkzeug.datastructures import FileStorage

from sample_db_utils.core.postgis_accessor import PostgisAccessor
from sample_db_utils.core.utils import validate_mappings, unzip, is_stream, reproject



class Driver(metaclass=ABCMeta):
    """Generic interface for data reader"""
    def __init__(self, storager, user=None, system=None):
        """
        Args:
            storager (Storager) - Storager Strategy. See @postgis_acessor
            user (sample_db.models.User) - The user instance sample owner
            system (lccs_db.models.LucClassificationSystem)
                The land use coverage classification system
        """

        if storager is None:
            storager = PostgisAccessor()

        self.storager = storager
        self.user = user
        self.system = system
        self._data_sets = []

    @abstractmethod
    def load(self, file):
        """Opens the file and load data"""

    @abstractmethod
    def load_classes(self, file):
        """Load sample classes in memory"""

    @abstractmethod
    def get_files(self):
        """Retrieves list of files to load"""

    def get_data_sets(self):
        """Retrieves the loaded data sets
        Returns:
            list of dict - Loaded data sets
        """
        return self._data_sets

    def load_data_sets(self):
        """Load data sets in memory using database format"""
        files = self.get_files()

        for f in files:
            self.load(f)
            print("{} loaded in memory".format(f))

        return self

    def store(self, observation_table):
        """
        Store the observations into database using
        Storager strategy
        """
        self.storager.store_observations(self._data_sets, observation_table)

class CSV(Driver):
    """Defines a Base class for handle CSV data files
    Basically, a CSV is built with a mappings config.
    The config describes how to read the dataset in order to
    create a Brazil Data Cube sample. The `mappings`
    must include at least the required fields to fill
    a sample, such latitude, longitude and class_name fields.
    """

    def __init__(self, entries, mappings, storager=None, **kwargs):
        """
        Args:
            entries (string|io.IOBase) - The file entries
            mappings (dict) - CSV Mappings to Sample
            storager (PostgisAccessor) -
        """

        copy_mappings = deepcopy(mappings)

        validate_mappings(copy_mappings)

        super(CSV, self).__init__(storager, **kwargs)

        self.mappings = copy_mappings
        self.entries = entries

    def get_files(self):
        if is_stream(self.entries) or \
           os.path.isfile(self.entries):
            return [self.entries]

        files = os.listdir(self.entries)

        return [
            os.path.join(self.entries, f) for f in files if f.endswith(".csv")
        ]

    def build_data_set(self, csv):
        """Build data set sample observation
        Args:
            csv(pd.DataFrame) - Open CSV file
        Returns:
            GeoDataFrame CSV with geospatial location
        """

        geom_column = [
            Point(xy) for xy in zip(csv['longitude'], csv['latitude'])
        ]
        geocsv = GeoDataFrame(csv,
                              crs=self.mappings.get('srid', 4326),
                              geometry=geom_column)

        geocsv['location'] = geocsv['geometry'].apply(
            lambda point: ';'.join(['SRID=4326', point.wkt])
        )

        geocsv['class_id'] = geocsv[self.mappings['class_name']].apply(
            lambda row: self.storager.samples_map_id[row]
        )

        start_date = self.mappings['start_date'].get('value') or \
            geocsv[self.mappings['start_date']['key']]

        end_date = self.mappings['end_date'].get('value') or \
            geocsv[self.mappings['end_date']['key']]

        collection_date = self.mappings['collection_date'].get('collection_date') or \
                   geocsv[self.mappings['collection_date']['key']]

        geocsv['user_id'] = self.user
        geocsv['start_date'] = start_date
        geocsv['end_date'] = end_date
        geocsv['collection_date'] = collection_date

        del geocsv['geometry']
        del geocsv['latitude']
        del geocsv['longitude']

        # Delete id column to avoid DuplicateError on database
        if 'id' in geocsv.columns:
            del geocsv['id']

        return geocsv

    def get_unique_classes(self, csv):
        """Retrieves distinct sample classes from CSV datasource"""
        return csv[self.mappings['class_name']].unique()

    def load(self, file):
        csv = pd.read_csv(file)

        self.load_classes(csv)

        res = self.build_data_set(csv)

        self._data_sets.extend(res.T.to_dict().values())

    def load_classes(self, file):
        self.storager.load()

        unique_classes = self.get_unique_classes(file)

        samples_to_save = []

        stored_keys = self.storager.samples_map_id.keys()

        for class_name in unique_classes:
            if class_name in stored_keys:
                continue

            sample_class = {
                "name": class_name,
                "description": class_name,
                "code": class_name,
                "class_system_id": self.system.id,
                # "user_id": self.user
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self.storager.store_classes(samples_to_save)
            self.storager.load()

class Shapefile(Driver):
    """Base class for Shapefiles Reader"""
    def __init__(self, entries, mappings, storager=None, **kwargs):
        copy_mappings = deepcopy(mappings)

        validate_mappings(copy_mappings)

        super(Shapefile, self).__init__(storager, **kwargs)

        self.mappings = copy_mappings
        self.entries = entries
        self.temporary_folder = TemporaryDirectory()
        self.class_name = None
        self.start_date = None
        self.end_date = None
        self.collection_date = None
        self.crs = None

    def get_unique_classes(self, ogr_file, layer_name):
        """Retrieves distinct sample classes from shapefile datasource"""

        classes = self.mappings.get('class_name')

        if isinstance(classes, str):
            classes = [self.mappings['class_name']]

        layer = ogr_file.GetLayer(layer_name)

        if layer.GetFeatureCount() == 0:
            return []

        f = layer.GetFeature(0)

        fields = [
            f.GetFieldDefnRef(i).GetName() for i in range(f.GetFieldCount())
        ]

        for possibly_class in classes:
            if possibly_class in fields:
                self.class_name = possibly_class

                return ogr_file.ExecuteSQL(
                    'SELECT DISTINCT "{}" FROM {}'.format(
                        possibly_class, layer_name))
        return []

    def get_files(self):
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
        """Build data set sample observation"""
        geometry = feature.GetGeometryRef()

        reproject(geometry, self.crs, 4326)

        geom_shapely = geom_from_wkt(
            geometry.ExportToWkt())

        ewkt = shape.from_shape(geom_shapely, srid=4326)

        start_date = self.mappings['start_date'].get('value') or \
            feature.GetField(self.mappings['start_date']['key'])

        end_date = self.mappings['end_date'].get('value') or \
            feature.GetField(self.mappings['end_date']['key'])

        # TODO
        collection_date = self.mappings['collection_date']

        return {
            "start_date": start_date,
            "end_date": end_date,
            "collection_date": collection_date,
            "location": ewkt,
            "class_id": self.storager.samples_map_id[feature.GetField(self.mappings['class_name'])] ,
            "user_id": self.user
        }

    def load(self, file):

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
        # Retrieves Layer Name from Data set filename
        layer_name = Path(file.GetName()).stem
        # Load Storager classes in memory
        self.storager.load()

        unique_classes = self.get_unique_classes(file, layer_name)

        samples_to_save = []

        for feature_id in range(unique_classes.GetFeatureCount()):
            feature = unique_classes.GetFeature(feature_id)
            class_name = feature.GetField(0)

            # When class already registered, skips
            if class_name in self.storager.samples_map_id.keys():
                continue

            sample_class = {
                "name": class_name,
                "description": class_name,
                "code": class_name,
                "class_system_id": self.system.id
            }

            samples_to_save.append(sample_class)

        if samples_to_save:
            self.storager.store_classes(samples_to_save)
            self.storager.load()