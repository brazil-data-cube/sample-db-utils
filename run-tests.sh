#!/usr/bin/env bash
#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
pydocstyle sample_db_utils setup.py && \
isort sample_db_utils tests setup.py --check-only --diff && \
check-manifest --ignore ".drone.yml,.readthedocs.yml" && \
sphinx-build -qnW --color -b doctest docs/sphinx/ docs/sphinx/_build/doctest && \
pytest