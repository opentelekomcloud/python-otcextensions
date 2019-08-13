============
Installation
============

There are several ways to install python-otcextensions to enhance the native ``openstack`` CLI client and to extend the OpenStack SDK to cover the additional Open Telekom Cloud services providing a larger functionality on top of OpenStack.

The easiest way is to use the Python pip installer which is working distribution independent and can be used in an isolated virtual environment as described below. Ansible can be used to install python-otcextensions on various operating systems, too by using the following Ansible Role: https://github.com/OpenTelekomCloud/ansible-role-otcextensions .
There are also ready-made installation packages for various operating systems which have their own versions, package names and sometimes bugs. A repository based on openSUSE's build services tries to cover these issues which is available under: https://build.opensuse.org/project/show/Cloud:OTC:Tools:OpenStack.

Overview of Related Packages
----------------------------

**OpenStackSDK:** 
  A library on the client side that translates Python function calls into API calls to an OpenStack cloud.
**OpenStackClient:** 
  An application that turns the Python interface of OpenStackSDK and python-otcextensions into a CLI tool.
**python-otcextensions:** 
  An addition to OpenStackSD with enhanced functionality that is specific for the Open Telekom Cloud.

Installation with pip installer
-------------------------------

All three packages are written in Python and stored as Python libraries in the PyPi repository. The following section describes the installation of ``OpenStackSDK``, ``otcextensions`` and ``OpenStackClient``. Please remember, it is not the latest development state. For this purpose the latest sources needs to be installed.

Installation under Ubuntu or Debian
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3 with developer libraries, and package manager pip are required:

.. code-block:: bash

   $ sudo apt update
   $ sudo apt install gcc python3 python3-dev python3-pip libssl-dev

Now, install all libraries and programs at once with the Python package manager pip. The --user flag provides user wide installation instead of a global installation.

.. code-block:: bash

    $ pip3 install otcextensions python-openstackclient --user


Installation under CentOS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3 with developer libraries, and package manager pip are required. If you want to use python3 which is recommended, you need to install the epel repository, first:


.. code-block:: bash

   $ sudo yum update 
   $ sudo yum install epel-release
   $ sudo yum install gcc python36 python36-devel python36-pip openssl-devel


Now, install all libraries and programs at once with the Python package manager pip:

.. code-block:: bash

   $ pip3 install otcextensions python-openstackclient --user

Installation under Fedora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3 with developer libraries, and package manager pip are required:


.. code-block:: bash

   $ sudo dnf upgrade
   $ sudo dnf install gcc python3 python3-devel python3-pip openssl-devel

Now, install all libraries and programs at once with the Python package manager pip:

.. code-block:: bash

   $ pip3 install otcextensions python-openstackclient --user
   

Installation in a virtual environment with pip installer
--------------------------------------------------------------

A virtual environment seperates your installed packages from other libraries and should be used as well.

Installation under Ubuntu or Debian
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3 with developer libraries, package manager, and virtual environment are required:

.. code-block:: bash

   $ sudo apt update
   $ sudo apt install gcc python3 python3-dev python3-pip python3-venv libssl-dev

A virtual environment seperates your installed packages from other libraries and should be used as well. You can name the virtual environment on your own desires, in our example it is: "venv". The second command will switch on "venv":

.. code-block:: bash

    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $

Now, install all libraries and programs at once with the Python package manager pip:

.. code-block:: bash

    $ pip install otcextensions openstackclient


Installation under CentOS
^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3 with developer libraries, package manager, and virtual environment are required.
If you want to use python3 which is recommended, you need to install the epel repository, first:


.. code-block:: bash

   $ sudo yum update 
   $ sudo yum install epel-release

No the python packages are needed:

.. code-block:: bash

   $ sudo yum update
   $ sudo yum install gcc python36 python36-devel python-pip python-virtualenv openssl-devel

A virtual environment seperates your installed packages from other libraries and should be used as well. You can name the virtual environment on your own desires, in our example it is: "venv". The second command will switch on "venv":

.. code-block:: bash

   $ python3 -m venv venv
   $ source venv/bin/activate

Now, install all libraries and programs at once with the Python package manager pip:

.. code-block:: bash

   $ pip install otcextensions openstackclient

Installation under Fedora (under review)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the installation, following packages are required: a C compiler, Python3 with developer libraries, package manager, and a virtual environment are required:


.. code-block:: bash

   $ sudo dnf upgrade
   $ sudo dnf install gcc python3 python3-devel python3-pip python3-virtualenv openssl-devel

The virtual environment will be created and activated. You can name the virtual environment on your own desires, in our example it is "venv":

.. code-block:: bash

   $ python3 -m venv venv
   $ source venv/bin/activate

Now, install all libraries and programs at once with the Python package manager pip:

.. code-block:: bash

   (venv) $ pip install otcextensions openstackclient
   

Installation from Github sources
--------------------------------

The latest state of the packages can be installed with the following approach.

Cloning the Github repository:

.. code-block:: bash

   $ git clone https://github.com/OpenTelekomCloud/python-otcextensions.git

A virtual environment seperates your installed packages from other libraries and should be used as well. You can name the virtual environment on your own desires, in our example it is: "venv". The second command will switch on "venv":

.. code-block:: bash

   $ python3 -m venv venv
   $ source venv/bin/activate
   (venv) $

Switch into the new folder which is created by cloning the repository and install install the project dependencies into the virtual environment:

.. code-block:: bash

   (venv) $ cd ./python-otcextensions

Register the CLI plugin using:

.. code-block:: bash

   (venv) ~/python-otcextensions$ python setup.py install
   
Install Openstack-Client binary from pip-Repository:

.. code-block:: bash

   (venv) ~/python-otcextensions$ pip install openstackclient

Configuration for the Cloud Connection
--------------------------------------

You can connect to the Open Telekom Cloud and OpenStack clouds in general using two approaches. The first one uses a credential file called ``clouds.yaml`` and the other one is to use environment variables.

Configuring a clouds.yaml file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The credential file clouds.yaml will be queried automatically in different locations with increasing precedence:

1. system-wide (/etc/openstack/{clouds,secure}.yaml)
2. Home directory / user space (~/.config/openstack/{clouds,secure}.yaml)
3. Current directory (./{clouds,secure}.yaml)

A sample clouds.yaml file is listed below to connect with Open Telekom Cloud:

**clouds.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        username: 'USER_NAME'
        password: 'PASS'
        project_name: 'eu-de'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
        user_domain_name: 'OTC00000000001000000xxx'
      interface: 'public'
      identity_api_version: 3 # !Important
      ak: 'AK_VALUE' # AK/SK pair for access to OBS
      sk: 'SK_VALUE'

The name otc is self-defined and can be changed. AK/SK values required for access to some services (i.e. OBS) can be either configured as shown above in the clouds.yaml/secure.yaml, or they can be automatically retrieved from the S3_ACCESS_KEY_ID and S3_SECRET_ACCESS_KEY. 

Additional connections to other Openstack-clouds or -projects can be added to the file as shown below:

**clouds.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        username: 'USER_NAME'
        password: 'PASS'
        project_name: 'eu-de'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
        user_domain_name: 'OTC00000000001000000xxx'
      interface: 'public'
      identity_api_version: 3 # !Important
      ak: 'AK_VALUE' # AK/SK pair for access to OBS
      sk: 'SK_VALUE'
    otcsecondproject:
      region_name: eu-de
      auth:
        username: '<USERNAME2>'
        password: '<PASSWORD2>'
        project_id: '<PROJECT-ID2>'
        user_domain_id: '<DOMAIN-ID2>'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'

Test your connection
^^^^^^^^^^^^^^^^^^^^

Use the following command to test the basic functionality.

.. code-block:: bash

   $ openstack --os-cloud otc flavor list

Splitting the credentials in clouds.yaml and secure.yaml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In some scenarios a split of security credentials from the configuration file is necessary. The optional file ``secure.yaml`` can be used to store the secret which is left out from ``clouds.yaml``:

**clouds.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        username: 'USER_NAME'
        project_name: 'eu-de'
        auth_url: 'https://iam.eu-de.otc.t-systems.com:443/v3'
        user_domain_name: 'OTC00000000001000000xxx'
      interface: 'public'
      identity_api_version: 3 # !Important
      ak: 'AK_VALUE' # AK/SK pair for access to OBS
      sk: 'SK_VALUE'

**secure.yaml**

.. code-block:: yaml

  clouds:
    otc:
      auth:
        password: '<PASSWORD>'

Configuration of Environment Variables
--------------------------------------

Instead of using the clouds.yaml file, environmnt variables can be configured to connect to the Open Telekom Cloud. Create a simple file like ``.ostackrc`` in the home directory and source the file to make the variables available. On Open Telekom Cloud servers this file exists on bootup and needs to be changed according to your credentials.

.. code-block:: bash

  export OS_AUTH_URL=<url-to-openstack-identity>
  export OS_IDENTITY_API_VERSION=3
  export OS_PROJECT_NAME=<project-name>
  export OS_PROJECT_DOMAIN_NAME=<project-domain-name>
  export OS_USERNAME=<username>
  export OS_USER_DOMAIN_NAME=<user-domain-name>
  export OS_PASSWORD=<password>  # (optional)
  export S3_ACCESS_KEY_ID=<access_key>
  export S3_SECRET_ACCESS_KEY=<secret_access_key>

Test your connection
^^^^^^^^^^^^^^^^^^^^

Use the following command to test the basic functionality.

.. code-block:: bash

   $ openstack flavor list
