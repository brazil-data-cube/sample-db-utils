Installation
============

Please, read the instructions below in order to install ``sample-db-utils``.

Development Installation - GitHub
---------------------------------

Clone the Software Repository
+++++++++++++++++++++++++++++


Use ``git`` to clone the software repository::

    git clone https://github.com/brazil-data-cube/sample-db-utils.git


Install sample-db-utils in Development Mode
+++++++++++++++++++++++++++++++++++++++++++


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

Run the Tests
+++++++++++++


.. code-block:: shell

     ./run-tests.sh




Build the Documentation
+++++++++++++++++++++++


You can generate the documentation based on Sphinx with the following command::

    python setup.py build_sphinx


The above command will generate the documentation in HTML and it will place it under::

    docs/sphinx/_build/html/


You can open the above documentation in your favorite browser, as::

    firefox docs/sphinx/_build/html/index.html
