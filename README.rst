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

Currently, several projects systematically provide information on the dynamics of land use and cover. Well known projects include PRODES, DETER and TerraClass. These projects are developed by INPE and they produce information on land use and coverage used by the Brazilian Government to make public policy decisions. Besides these projects there are other initiatives from universities and space agencies devoted to the creation of national and global maps.

These data products are generated using different approaches and methodologies. In this context, the data set used in the sample and validation plays a fundamental role in the classification algorithms that generate new land use and coverage maps. A classified map’s accuracy depends directly on the quality of the training samples used by the machine learning methods.

Land use and cover samples are collected by different projects and individuals, using different methods, such as in situ gathering in fieldwork and visual interpretation of high-resolution satellite images. An important requirement is to be able to describe samples with proper metadata that characterize their differences and organize them in a shared database to facilitate the reproducibility of experiments. It is also important to develop tools to easily discover, query, access, and process this shared sample database.

Sample-DB (Sample Database) provides a data model that represents the land use and cover samples collected by different projects and individuals. **SAMPLE-DB-UTILS**, has the utility functions that perform the transformation of different data formats to be stored by SAMPLE-DB.

This package is related to other softwares in the Brazil Data Cube project. For more information on SAMPLE-DB-UTILS, see:

- `LCCS-DB <https://github.com/brazil-data-cube/sample-db>`_: Land Cover Classification System Database Model.
- `SAMPLE-DB <https://github.com/brazil-data-cube/sample-db>`_: Sample Database Model.
- `SAMPLE.py <https://github.com/brazil-data-cube/sample.py>`_: Python client library over a WFS endpoint for retrieving samples.

Installation
============


See `INSTALL.rst <./docs/sphinx/installation.rst>`_.


License
=======


.. admonition::
    Copyright (C) 2020-2021 INPE.

    SAMPLE-DB is a free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.