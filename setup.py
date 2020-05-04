#
# This file is part of Sample Database Utils.
# Copyright (C) 2019 INPE.
#
# Sample Database Utils is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Sample Database Utils Setup"""


import os
from setuptools import find_packages, setup

readme = open('README.rst').read()

docs_require = [
    'bdc-readthedocs-theme @ git+git://github.com/brazil-data-cube/bdc-readthedocs-theme.git#egg=bdc-readthedocs-theme',
    'Sphinx>=2.1.2',
]

tests_require = [
    'pytest>=5.0.0,<6.0.0',
]

install_requires = [
    'geopandas>=0.5.0',
    # 'gdal>=2.3.3,<3',
    'SQLAlchemy[postgresql]>=1.3.4',
    'GeoAlchemy2>=0.6.2',
    'psycopg2>=2.8.3',
    'requests>=2.9.1',
    'shapely>=1.6',
     'lccs-db @ git+git://github.com/brazil-data-cube/lccs-db.git#egg=lccs-db',
]

extras_require = {
    'docs': docs_require,
    'tests': tests_require,
}

setup_requires = [
    'pytest-runner>=5.2',
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