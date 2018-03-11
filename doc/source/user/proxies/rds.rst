Database RDS API
================

For details on how to use database, see :doc:`/user/guides/rds`

.. automodule:: otcextensions.sdk.rds.v1._proxy

The Database Class
------------------

The database high-level interface is available through the ``database``
member of a :class:`~otcextensions.connection.Connection` object.  The
``database`` member will only be added if the service is detected.

Flavor Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.get_flavor
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.find_flavor
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.flavors

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.create_instance
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.update_instance
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.delete_instance
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.get_instance
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.find_instance
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.instances
