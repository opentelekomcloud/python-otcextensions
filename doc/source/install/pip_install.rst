Installation with PiP Installer
===============================

All three packages are written in Python and stored as Python packages in the
PyPi repository. The following section describes the installation of
``OpenStackSDK``, ``otcextensions`` and ``OpenStackClient``. Please remember,
it is not the latest development state. For this purpose the latest sources
needs to be installed.

PiP Installation in User Space
------------------------------

Ubuntu or Debian
^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3
with developer libraries, and package manager pip are required:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install gcc python3 python3-dev python3-pip libssl-dev

Now, install all libraries and programs at once with the Python package
manager pip. The --user flag provides user wide installation instead of a
global installation.

.. code-block:: bash

    $ pip3 install otcextensions python-openstackclient --user


CentOS
^^^^^^

For the installation, following packages are required: a C compiler, Python3
with developer libraries, and package manager pip are required. If you want to
use python3 which is recommended, you need to install the epel
repository, first:

.. code-block:: bash

    $ sudo yum update
    $ sudo yum install epel-release
    $ sudo yum install gcc python36 python36-devel python36-pip openssl-devel

Now, install all libraries and programs at once with the Python package
manager pip:

.. code-block:: bash

    $ pip3 install otcextensions python-openstackclient --user

Fedora
^^^^^^

For the installation, following packages are required: a C compiler, Python3
with developer libraries, and package manager pip are required:


.. code-block:: bash

    $ sudo dnf upgrade
    $ sudo dnf install gcc python3 python3-devel python3-pip openssl-devel

Now, install all libraries and programs at once with the Python package
manager pip:

.. code-block:: bash

    $ pip3 install otcextensions python-openstackclient --user

PiP Installation within a Virtual Environment
---------------------------------------------

A virtual environment seperates your installed packages from other
libraries and should be used as well.

Ubuntu or Debian
^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3
with developer libraries, package manager, and virtual environment
are required:

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install gcc python3 python3-dev python3-pip python3-venv libssl-dev

A virtual environment seperates your installed packages from other libraries
and should be used as well. You can name the virtual environment on your own
desires, in our example it is: "venv". The second command will switch
on "venv":

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $

Now, install all libraries and programs at once with the Python package
manager pip:

.. code-block:: bash

    $ pip install otcextensions openstackclient


CentOS
^^^^^^

For the installation, following packages are required: a C compiler, Python3
with developer libraries, package manager, and virtual environment are
required. If you want to use python3 which is recommended, you need to
install the epel repository, first:


.. code-block:: bash

    $ sudo yum update
    $ sudo yum install epel-release

No the Python packages are needed:

.. code-block:: bash

    $ sudo yum update
    $ sudo yum install gcc python36 python36-devel python-pip \
      python-virtualenv openssl-devel

A virtual environment seperates your installed packages from other libraries
and should be used as well. You can name the virtual environment on your own
desires, in our example it is: "venv". The second command will switch
on "venv":

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate

Now, install all libraries and programs at once with the Python package
manager pip:

.. code-block:: bash

    $ pip install otcextensions openstackclient

Fedora (under review)
^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler,
Python3 with developer libraries, package manager, and a virtual
environment are required:

.. code-block:: bash

    $ sudo dnf upgrade
    $ sudo dnf install gcc python3 python3-devel python3-pip \
      python3-virtualenv openssl-devel

The virtual environment will be created and activated. You can name the
virtual environment on your own desires, in our example it is "venv":

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate

Now, install all libraries and programs at once with the Python package
manager pip:

.. code-block:: bash

    (venv) $ pip install otcextensions openstackclient