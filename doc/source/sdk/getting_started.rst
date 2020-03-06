Getting Started
===============

Connect to the cloud
--------------------

In order to work with an OpenStack cloud you first need to create a
:class:`~openstack.connection.Connection` using your credentials. A
:class:`~openstack.connection.Connection` can be created in three
ways, using the class itself, :ref:`config-clouds-yaml`, or
:ref:`config-environment-variables`. It is recommended use
:ref:`config-clouds-yaml` as the same config can be used across tools
and languages. Examples are the OpenStack Client, the Gophercloud
library for golang, and Terraform that is based on that
library. Please be also aware that environment variables carrying
credentials can be a security risk.

Create Connection
^^^^^^^^^^^^^^^^^

To create a :class:`~openstack.connection.Connection` instance, use the
:func:`~openstack.connect` factory function.

As a next step inject the OTC Extensions into the retrieved connection

.. code-block:: python

   # An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
   conn = openstack.connect(cloud='otc')

   # Register OTC Extensions
   sdk.register_otc_extensions(conn)

See a full example at `connect_otc.py <examples/connect_otc.py>`_

.. note:: To enable logging, see the `<guides/logging.rst>`_ user guide.

Verify Installation
^^^^^^^^^^^^^^^^^^^

You need to have the OpenStack SDK in package `openstacksdk` installed
to work with the OTC Extensions, which are packaged in
`otcextensions`. Thanks to a plugin mechanism, no additional
configuration is needed to use the extension. To verify you are up and
running write a file `demo.py`:

.. code-block: python

    import openstack as mycloud

    conn = mycloud.connect("otc")
    conn.jjjjj.flavors()
    
Make sure that you configured your credentials as describe in the
`configuration` section. Run this script with

.. code-block: bash
    $ python demo.py

It should XXXXXXXX list your XXXXXXXX.

    
with this Python script and run it with
`python demo.py`.