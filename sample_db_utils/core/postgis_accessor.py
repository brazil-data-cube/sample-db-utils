#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Postgis Accessor Class."""

from lccs_db.models import LucClass, db


class PostgisAccessor(object):
    """Postgis Acessor Class."""

    def __init__(self):
        """Init method."""
        self.sample_classes = []
        self.samples_map_id = {}

    def store_classes(self, classes):
        """Insert multiple sample classes on database.

        Args:
            classes (dict[]): list List of classes objects to save
        """
        db.session.bulk_insert_mappings(LucClass, classes)
        db.session.commit()

    def store_observations(self, data_sets, observation_table):
        """Store sample observation into database.

        Args:
            data_sets (dict[]): List of data sets observation to store
        """
        db.engine.execute(
            observation_table.insert(),
            data_sets
        )
        db.session.commit()

    def load(self):
        """Load sample classes in memory."""
        self.sample_classes = LucClass.filter()
        self.samples_map_id = {}

        for sample in self.sample_classes:
            self.samples_map_id[sample.name] = sample.id