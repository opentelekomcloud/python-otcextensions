Getting Started
===============

Verify Installation
-------------------

``OTC Extensions`` needs to be installed correctly. Please check
:doc:`../install/index` for further instructions. The
``otcextensions`` Python package pulls the ``openstacksdk`` package
automatically as dependency which is needed to create own OpenStack scripts.

Configure Connection Credentials
--------------------------------

In order to work with an OpenStack cloud you first need to create a
:class:`~openstack.connection.Connection` using your credentials. A
:class:`~openstack.connection.Connection` can be created in three
ways, using the class itself, :ref:`clouds-yaml`, or
:ref:`environment-variables`. It is recommended use
:ref:`clouds-yaml` as the same config can be used across tools
and languages. Examples are:

- OpenStack Client
- Gophercloud (library for golang)
- Terraform (based on Gophercloud)

.. note:: Please be also aware that environment variables carrying
   credentials can be a security risk.


Creating a Minimal Python Script
--------------------------------

At first we need to import `openstack` to get access to all available
:doc:`Proxy <proxies/index>` functions. Enable Logging is an optional
step in the script and can be left out in productive usage.
For communication purposes a :class:`~openstack.connection.Connection`
instance is created to communicate with the Cloud environment. The
`cloud=<NAME>` represents the :class:`~openstack.connection.Connection`
name defined while creating the ``clouds.yaml`` file in :ref:`clouds-yaml`.
The ``cloud``-variable can be left out if environment variables are
used or only ``one`` Cloud-connection is defined.

.. code-block:: python

   #!/usr/bin/env python3

   import openstack

   # optional, enable Logging on
   openstack.enable_logging(True)

   # Creates cloud connection
   # Parameter cloud='otc' is optional for env variables or single
   # clouds.yaml entry.
   conn = openstack.connect(cloud='otc', vendor_hook="otcextensions.sdk:load")

   for server in conn.compute.servers():
       print(server)

.. note:: For further examples, see `Examples <examples>`_.

.. note:: For further information about logging, please see
   :doc:`Logging User Guide <guides/logging>`.

Run the Script
--------------

After saving the script as `list_server.py`. You can simply run it by using
the following command.

.. code-block:: bash

   python list_server.py

The output represents all existent OpenStack servers in your Cloud
environment.

OTC Extensions specific Example for Open Telekom Cloud
------------------------------------------------------

The following script uses the OTC Extensions to list all existent CCE Clusters
in your account.

.. code-block:: python

   #!/usr/bin/env python3

   import openstack

   # openstack.enable_logging(True)
   conn = openstack.connect(vendor_hook="otcextensions.sdk:load")

   for cluster in conn.cce.clusters():
       print(cluster)

Save the file as `list_cce_clusters.py` and run it with:

.. code-block:: bash

   python list_cce_clusters.py
