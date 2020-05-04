#
# This file is part of Sample Database Utils.
# Copyright (C) 2019 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

""" Sample DB Utils Factory"""

from sample_db_utils.core.driver import CSV, Shapefile


class DriverFactory:
    """
    Defines a list of loaded drivers responsible to read
    samples dataset
    A driver consists in an implementation of
    sample_db_utils.core.driver.Driver. By default, we support both CSV
    and Shapefile samples. These drivers are attached to the
    HTTP content type.
    TODO: Read external drivers using entrypoints pkg_resources
    """

    drivers = {
        'text/csv': CSV,
        'application/vnd.ms-excel': CSV,
        'application/zip': Shapefile,
        'application/x-zip-compressed': Shapefile
    }

    def add(self, driver_name, driver):
        """
        Add a new driver into factory for handle sample
        by content type
        Args:
            driver_name (str): Content type of Driver.
            driver (Driver): Driver Class handler
        """
        self.drivers[driver_name] = driver

    def get(self, driver_name):
        """Retrieves a loaded driver from content type"""
        assert driver_name in self.drivers

        return self.drivers[driver_name]


factory = DriverFactory()