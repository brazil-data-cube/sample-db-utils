# This file is part of Sample Database Utils.
# Copyright (C) 2019 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

""" Brazil Data Cube Class."""

from ..core.driver import Shapefile

class HugoTese(Shapefile):
    """Driver for data loading to `sampledb`"""

    def __init__(self, entries, storager, **kwargs):

        mappings = dict(
            class_name="obs",
            start_date=dict(value='2015-09-01'),
            end_date=dict(value='2016-08-31'),
            collection_date= None
        )

        super(HugoTese, self).__init__(entries, mappings, storager, **kwargs)