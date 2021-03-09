#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Test for sample-db-utils operation."""
import datetime

from sample_db_utils.core.utils import get_date_from_str


def test_get_date_from_str():
    test_date = datetime.datetime(2014, 2, 4, 0, 0)
    date = get_date_from_str("04-02-2014")

    assert test_date == test_date.strptime(date, '%Y-%m-%d')
    assert isinstance(date, str)
