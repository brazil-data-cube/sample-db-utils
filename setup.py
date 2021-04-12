#
# This file is part of Sample Database Utils.
# Copyright (C) 2020-2021 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Sample Database Utils."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

history = open('CHANGES.rst').read()

tests_require = [
    'coverage>=4.5',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'pydocstyle>=4.0',
    'isort>4.3',
    'check-manifest>=0.40',
    'requests-mock>=1.7.0',
]

docs_require = [
    'Sphinx>=2.2',
    'sphinx_rtd_theme',
    'sphinx-copybutton',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

extras_require['all'] = [req for exts, reqs in extras_require.items() for req in reqs]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'geopandas>=0.5.0',
    'GeoAlchemy2>=0.6.2',
    'requests>=2.9.1',
    'shapely>=1.6',
    'GDAL>=2.2',
    'lccs-db @ git+https://github.com/brazil-data-cube/lccs-db.git@v0.6.0',
]

packages = find_packages()

r_data = os.path.join('sample_db_utils', '/drives/r-scripts/*.R')

package_data = {
    'r-scripts': [r_data,
                  ],
}


with open(os.path.join('sample_db_utils', 'version.py'), 'rt') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='sample_db_utils',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n',
    keywords='',
    license='MIT',
    author='INPE',
    author_email='',
    url='https://github.com/brazil-data-cube/sample-db-utils.git',
    packages=packages,
    zip_safe=False,
    package_data=package_data,
    include_package_data=True,
    platforms='any',
    entry_points={
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 3 - Alpha',
    ],
)
