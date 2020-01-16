Connect to the cloud
====================

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
-----------------

To create a :class:`~openstack.connection.Connection` instance, use the
:func:`~openstack.connect` factory function.

As a next step inject the OTC Extensions into the retrieved connection

.. code-block:: python

   # An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
   conn = openstack.connect(cloud='otc')

   # Register OTC Extensions
   sdk.register_otc_extensions(conn)

See a full example at `connect_otc.py <examples/connect_otc.py>`_

.. note:: To enable logging, see the :doc:`logging` user guide.

Next
----

Now that you can create a connection, continue with the :ref:`user_guides`
to work with an OpenStack service.
