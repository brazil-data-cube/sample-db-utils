# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Brazil Data Cube Class."""

from ..core.driver import Shapefile


class Hugo(Shapefile):
    """Driver for data loading to sampledb."""

    def __init__(self, entries, storager, **kwargs):
        """Init method."""
        mappings = dict(
            class_name="level2",
            end_date=dict(value='2019-08-31'),
            start_date=dict(value='2018-09-01'),
            collection_date= None
        )

        super(Hugo, self).__init__(entries, mappings, storager, **kwargs)