Installation from GitHub sources
================================

The latest state of the packages can be installed with the following
source installation approach.

Cloning the Github repository:

.. code-block:: bash

    $ git clone https://github.com/OpenTelekomCloud/python-otcextensions.git

A virtual environment seperates your installed packages from other libraries
and should be used as well. You can name the virtual environment on your own
desires, in our example it is: "venv". The second command will switch
on "venv":

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $

Switch into the new folder which is created by cloning the repository and
install install the project dependencies into the virtual environment:

.. code-block:: bash

    (venv) $ cd ./python-otcextensions

Register the CLI plugin using:

.. code-block:: bash

    (venv) ~/python-otcextensions$ python setup.py install

Install Openstack-Client binary from pip-Repository:

.. code-block:: bash

    (venv) ~/python-otcextensions$ pip install openstackclient
