#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Test for sample-db-utils operation."""
import datetime
import json

import pytest

from sample_db_utils.core.utils import get_date_from_str, validate_mappings


def test_get_date_from_str():
    test_date = datetime.datetime(2014, 2, 4, 0, 0)
    date = get_date_from_str("04-02-2014")

    assert test_date == test_date.strptime(date, '%Y-%m-%d')
    assert isinstance(date, str)


def test_validate_mappings():
    mappings_str = '{"class_name":"cons_1985","start_date":{"value":"1985-01-01"},"end_date":{"value":"1985-12-31"}}'
    validate_mappings(json.loads(mappings_str))


@pytest.mark.xfail(raises=TypeError)
def test_validate_mappings_fail():
    mappings_str = '{"class":"cons_1985","start_date":{"value":"1985-01-01"},"end_date":{"value":"1985-12-31"}}'
    validate_mappings(json.loads(mappings_str))
