..
    This file is part of Sample Database Utils.
    Copyright (C) 2020-2021 INPE.

    Sample Database Utils is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.


Installation
============

``sample-db-utils`` implementation depends essentially on `LCCS Database Module <https://github.com/brazil-data-cube/lccs-db>`_ and
`GDAL <https://gdal.org/>`_  ``(Version 2+)``.

Please, read the instructions below in order to install ``sample-db-utils``.


Production installation
-----------------------

Install from `GitHub <https://github.com/brazil-data-cube/sample-db-utils>`_::

        pip3 install git+https://github.com/brazil-data-cube/sample-db-utils

Development Installation
------------------------

Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/sample-db-utils.git

Go to the source code folder::

    cd sample-db-utils


Install in development mode::

    pip3 install -e .[all]


.. note::

    If you want to create a new *Python Virtual Environment*, please, follow this instruction:

    *1.* Create a new virtual environment linked to Python 3.7::

        python3 -m venv venv


    **2.** Activate the new environment::

        source venv/bin/activate


    **3.** Update pip and setuptools::

        pip3 install --upgrade pip

        pip3 install --upgrade setuptools

    Or you can use Python Anaconda Environment:

    **1.** Create an virtual environment using conda with Python Interpreter Version +3::

        conda create --name bdc_sample python=3

    **2.** Activate environment::

        conda activate bdc_sample


.. note::

    | If you have problems during the GDAL Python package installation, please, make sure to have the GDAL library support installed in your system with its command line tools.
    |
    | You can check the GDAL version with:
    | ``$ gdal-config --version``.
    |
    | Then, if you want to install a specific version (example: 2.4.2), try:
    | ``$ pip install "gdal==2.4.2"``
    |
    | If you still having problems with GDAL installation, you can generate a log in order to check what is happening with your installation. Use the following ``pip`` command:
    | ``$ pip install --verbose --log my.log "gdal==2.4.2"``
    |
    | You can install the GDAL in Anaconda Environment with:
    | ``$ conda install -c conda-forge gdal``
    | For more information, see [#f1]_ e [#f2]_.

Run the Tests
+++++++++++++

Run the tests::

     ./run-tests.sh


Build the Documentation
+++++++++++++++++++++++

You can generate the documentation based on Sphinx with the following command::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html

.. rubric:: Footnotes

.. [#f1] During GDAL installation, if you have a build message such as the one showed below

    .. code-block:: shell

        Skipping optional fixer: ws_comma
        running build_ext
        building 'osgeo._gdal' extension
        creating build/temp.linux-x86_64-3.7
        creating build/temp.linux-x86_64-3.7/extensions
        extensions/gdal_wrap.cpp:3168:10: fatal error: cpl_port.h: No such file or directory
         #include "cpl_port.h"
                  ^~~~~~~~~~~~
        compilation terminated.
        error: command 'x86_64-linux-gnu-gcc' failed with exit status 1
        Running setup.py install for gdal ... error
        Cleaning up...

    You can instruct ``pip`` to look at the right place for header files when building GDAL:

    .. code-block:: shell

        $ C_INCLUDE_PATH="/usr/include/gdal" \
          CPLUS_INCLUDE_PATH="/usr/include/gdal" \
          pip install "gdal==2.4.2"


.. [#f2] On Linux Ubuntu 18.04 LTS you can install GDAL 2.4.2 from the UbuntuGIS repository:

    | 1. Create a file named ``/etc/apt/sources.list.d/ubuntugis-ubuntu-ppa-bionic.list`` and
    | add the following content:

    .. code-block:: shell

        deb http://ppa.launchpad.net/ubuntugis/ppa/ubuntu bionic main
        deb-src http://ppa.launchpad.net/ubuntugis/ppa/ubuntu bionic main


    2. Then add the following key:

    .. code-block:: shell

        $ sudo apt-key adv --keyserver keyserver.ubuntu.com \
        --recv-keys 6B827C12C2D425E227EDCA75089EBE08314DF160


    3. Then, update your repository index:

    .. code-block:: shell

        $ sudo apt-get update


    4. Finally, install GDAL:

    .. code-block:: shell

        $ sudo apt-get install libgdal-dev=2.4.2+dfsg-1~bionic0