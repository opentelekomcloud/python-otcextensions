============
Installation
============

There are several ways to install python-otcextensions to enhance the native ``openstack`` CLI client and to extend the OpenStack SDK to cover the additional Open Telekom Cloud services providing a larger functionality on top of OpenStack.

The easiest way is to use the Python pip installer which is working distribution independent. 
There are also ready-made installation packages for various operating systems which have their own versions, package names and sometimes bugs. A repository based on openSUSE's build services tries to cover these issues which is available under: https://build.opensuse.org/project/show/Cloud:OTC:Tools:OpenStack.

Package Overview
---------------------

**openstacksdk:** 
  A library on the client side that translates API calls to an OpenStack cloud into Python function calls.
**otcextensions:** 
  An addition to openstacksdk with functionality that is specific for the Open Telekom Cloud.
**openstackclient:** 
  An application that turns the Python interface of openstacksdk and otcextensions into a CLI tool.

Installation via pip Installer
------------------------------

All three packages are written in Python and stored as Python libraries in the PyPi repository. The following section describes the installation of ``openstacksdk``, ``otcextensions`` and ``openstackclient``. Please remember, it is not the latest development state. For this purpose the latest sources needs to be installed.

Installation under Ubuntu or Debian with pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After a new installation: a C compiler, Python3 with developer libraries, package manager, and virtual environment are required:

.. code-block:: bash

   $ sudo apt update
   $ sudo apt install gcc python3 python3-dev python3-pip python3-venv libssl-dev

A virtual environment seperates your installed packages from other libraries and should be used as well. You can name the virtual environment on your own desires, in our example it is: "os-dev". The second command will switch on "os-dev":

.. code-block:: bash

    $ python3 -m venv os-dev
    $ source os-dev/bin/activate
    (os-dev) $

Now, install all libraries and programs at once with the Python package manager pip. The library wheel caches the built artifacts:

.. code-block:: bash

    $ pip install wheel openstacksdk otcextensions openstackclient


Installation under Fedora, Red Hat Enterprise Linux, or CentOS with pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After a new installation: a C compiler, Python3 with developer libraries, package manager, and virtual environment are required:

.. code-block:: bash

   $ sudo yum update
   $ sudo yum install gcc python3 python3-dev python3-pip python3-venv openssl-devel

A virtual environment seperates your installed packages from other libraries and should be used as well. You can name the virtual environment on your own desires, in our example it is: "os-dev". The second command will switch on "os-dev":

.. code-block:: bash

   $ python3 -m venv os-dev
   $ source os-dev/bin/activate

Now, install all libraries and programs at once with the Python package manager pip. The library wheel caches the built artifacts:

.. code-block:: bash

   $ pip install wheel openstacksdk otcextensions openstackclient


Installation from Github sources
--------------------------------

The latest state of the packages can be installed with the following approach.

Cloning the Github repository:

.. code-block:: bash

   $ git clone git@github.com:OpenTelekomCloud/python-otcextensions.git

A virtual environment seperates your installed packages from other libraries and should be used as well. You can name the virtual environment on your own desires, in our example it is: "os-dev". The second command will switch on "os-dev":

.. code-block:: bash

   $ python3 -m venv os-dev
   $ source os-dev/bin/activate

Switch into the new folder which is created by cloning the repository and install install the project dependencies into the virtual environment:

.. code-block:: bash

   $ cd ./python-otcextensions.git
   ~/python-otcextensions$ pip install -r requirements.txt

Register the CLI plugin using:

.. code-block:: bash

   ~/python-otcextensions$ python setup.py install
