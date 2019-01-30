Connect OTC
===========

In order to work with an OpenStack cloud you first need to create a
:class:`~openstack.connection.Connection` to it using your credentials. A
:class:`~openstack.connection.Connection` can be
created in 3 ways, using the class itself, :ref:`config-clouds-yaml`, or
:ref:`config-environment-variables`. It is recommended to always use
:ref:`config-clouds-yaml` as the same config can be used across tools and
languages.

Create Connection
-----------------

To create a :class:`~openstack.connection.Connection` instance, use the
:func:`~openstack.connect` factory function.

As a next step inject the OTC extensions into the retrieved connection

.. code-block:: python

   # An 'otc' is a cloud connection with name 'otc' configured in the clouds.yaml
   conn = openstack.connect(cloud='otc')

   # Register OTC Extensions
   sdk.register_otc_extensions(conn)

Full example at `connect_otc.py <examples/connect_otc.py>`_

.. note:: To enable logging, see the :doc:`logging` user guide.

Next
----
Now that you can create a connection, continue with the :ref:`user_guides`
to work with an OpenStack service.

.. TODO(shade) Update the text here and consolidate with the old
   os-client-config docs so that we have a single and consistent explanation
   of the envvars cloud, etc.
