#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Test for sample-db-utils operation."""
import json

import pytest

from sample_db_utils.core.driver import Driver
from sample_db_utils.factory import factory


def test_factory():
    """Test factory get type."""
    driver_klass = factory.get("application/zip")

    assert driver_klass.__class__.__name__ == "ABCMeta"
    assert driver_klass.__name__ == "Shapefile"


@pytest.mark.xfail(raises=TypeError)
def test_drive_create_fail():
    """Test drive creator by factory type."""
    driver_klass = factory.get("application/zip")
    driver: Driver = driver_klass(entries=None, mappings=None)

    assert driver.__class__ == "Shapefile"


def test_drive_create():
    """Test drive creator by factory type."""
    driver_klass = factory.get("application/zip")

    mappings_str = '{"class_name":"cons_1985","start_date":{"value":"1985-01-01"},"end_date":{"value":"1985-12-31"}}'
    mappings = json.loads(mappings_str)
    driver: Driver = driver_klass(entries=None, mappings=mappings)

    assert driver.__class__.__name__ == "Shapefile"
