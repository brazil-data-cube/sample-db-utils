#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Sample DB Utils Drives Factory."""

from .bdc import BDC
from .hugo import Hugo
from .hugo_tese import HugoTese
from .inSitu import InSitu


class DriversFactory:
    """Factory for Drives."""

    @staticmethod
    def make(driverType, entries, storager, **kwargs):
        """Make Factory method for creates datasource."""
        factorys = ["Cerrado", "VMaus", "Canasat", "Lapig", "Fototeca" , "Embrapa", "InSitu",  "BDC",
                    "Hugo", "HugoTese"]

        assert driverType in factorys

        driver = eval(driverType)(entries, storager, **kwargs)

        return driver