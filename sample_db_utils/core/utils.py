#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""This file contains code utilities of Brazil Data Cubes sampledb."""

import os
from datetime import datetime
from io import IOBase
from tempfile import SpooledTemporaryFile
from zipfile import ZipFile

import osgeo
from osgeo import osr
from werkzeug.datastructures import FileStorage


def validate_mappings(mappings):
    """Validate a class mappings of dataset table.

    A mapping consists in a dictionary which maps the expected keys with
    provided keys in dataset.
    The well-known properties are:
    - geom : Geometry field.
    - latitude: Latitude field (when geom is not provided)
    - longitude: Longitude field (when geom is not provided)
    - class_name: Sample class. Default is "label"
    - start_date: Start date field. Default is "start_date"
    - end_date: End date field. Default is "end_date"
    - collection_date: End date field. Default is "end_date"

    """
    def set_default_value_for(key, object_reference):
        obj = dict()

        value = object_reference.get(key)
        if isinstance(value, str):
            obj.update(dict(key=object_reference[key]))
        elif not value:
            obj.setdefault('key', key)
        else:
            obj.update(object_reference[key])

        object_reference[key] = obj

    if not mappings:
        raise TypeError('Invalid mappings')

    if not mappings.get('class_name'):
        mappings['class_name'] = 'label'

    if not mappings.get('geom'):
        if not mappings.get('latitude') and not mappings.get('longitude'):
            mappings['geom'] = 'geometry'

    set_default_value_for('start_date', mappings)
    set_default_value_for('end_date', mappings)
    set_default_value_for('collection_date', mappings)


def reproject(geom, source_srid, target_srid):
    """Reproject a geometry to srid provided.

    It may throws exception when SRID is invalid

    Args:
        geom (ogr.Geometry): Geometry
        source_srid (int): Input SRID
        target_srid (int): Target SRID

    """
    source = osr.SpatialReference()

    if isinstance(source_srid, int):
        source.ImportFromEPSG(source_srid)
    else:
        source.ImportFromProj4(source_srid)

    target = osr.SpatialReference()

    if isinstance(target_srid, int):
        target.ImportFromEPSG(target_srid)
    else:
        target.ImportFromProj4(target_srid)

    if int(osgeo.__version__[0]) >= 3:
        source.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        target.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)

    transform = osr.CoordinateTransformation(source, target)
    geom.Transform(transform)


def unzip(stream, destination):
    """Uncompress the zip file to the destination.

    The input may be a file or bytes representing opened file

    Args:
        stream (str, io.Bytes) - File to extract
        destination (str) - Destination directory

    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    with ZipFile(stream) as zip_object:
        zip_object.extractall(destination)


def is_stream(entry):
    """Return if the provided entry is readable as stream-like."""
    return isinstance(entry, IOBase) or \
           isinstance(entry, SpooledTemporaryFile) or \
           isinstance(entry, FileStorage)


def get_date_from_str(date):
    """Build date from str."""
    date = date.replace('/', '-')

    try:
        date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        date = datetime.strptime(date, '%d-%m-%Y').strftime('%Y-%m-%d')

    return date