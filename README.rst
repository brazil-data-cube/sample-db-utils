..
    This file is part of SAMPLE-DB-UTILS.
    Copyright (C) 2020-2021 INPE.

    SAMPLE-DB-UTILS is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

====================================
Utility Functions for the SAMPLE-DB
====================================


.. image:: https://img.shields.io/badge/license-MIT-green
        :target: https://github.com/brazil-data-cube/sample-db-utils/blob/master/LICENSE
        :alt: Software License

.. image:: https://drone.dpi.inpe.br/api/badges/brazil-data-cube/sample-db-utils/status.svg
        :target: https://drone.dpi.inpe.br/brazil-data-cube/sample-db-utils
        :alt: Build Status

.. image:: https://codecov.io/gh/brazil-data-cube/sample-db-utils/branch/master/graph/badge.svg?token=FB89ZT9LX1
        :target: https://codecov.io/gh/brazil-data-cube/sample-db-utils
        :alt: Code Coverage Test

.. image:: https://readthedocs.org/projects/sample-db-utils/badge/?version=latest
        :target: https://sample-db-utils.readthedocs.io/en/latest/
        :alt: Documentation Status


.. image:: https://img.shields.io/badge/lifecycle-experimental-orange.svg
        :target: https://www.tidyverse.org/lifecycle/#experimental
        :alt: Software Life Cycle


.. image:: https://img.shields.io/github/tag/brazil-data-cube/sample-db-utils.svg
        :target: https://github.com/brazil-data-cube/sample-db-utils/releases
        :alt: Release


.. image:: https://img.shields.io/discord/689541907621085198?logo=discord&logoColor=ffffff&color=7389D8
        :target: https://discord.com/channels/689541907621085198#
        :alt: Join us at Discord


About
=====

The land use and land cover samples are stored in a database to assist in the experiments of the Brazil Data Cube. **SAMPLE-DB** has the data model and functions to consult and store the land use and land cover samples. This repository, **SAMPLE-DB-UTILS**, has the utility functions that perform the transformation of different data formats to be stored by SAMPLE-DB.
To facilitate access to samples of land use and land cover stored in the database, a Python package called **SAMPLE.py** was developed. This package retrieves the land use and land cover samples that were made available via WFS by the GeoServer application.

For more information on SAMPLE-DB-UTILS, see:

- `lccs-db <https://github.com/brazil-data-cube/sample-db>`_: Land Cover Classification System Database Model.
- `sample-db <https://github.com/brazil-data-cube/sample-db>`_: SQLAlchemy models and utility functions to query and store data.
- `sample.py <https://github.com/brazil-data-cube/sample.py>`_: Python client library over a WFS endpoint for retrieving samples.

Installation
============


See `INSTALL.rst <./docs/sphinx/installation.rst>`_.


License
=======


.. admonition::
    Copyright (C) 2020-2021 INPE.

    SAMPLE-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.