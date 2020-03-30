Database RDS API
================

For details on how to use database, see /user/guides/rds (NEEDS TO BE DONE)

.. automodule:: otcextensions.sdk.rds.v1._proxy

The Database Class
------------------

The database high-level interface is available through the ``rds`` member of a
:class:`~openstack.connection.Connection` object.  The ``rds`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Datastore Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.datastore_versions
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.get_datastore_version
   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.datastore_types

Flavor Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.get_flavor
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


Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.backups
  .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.create_backup
  .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.delete_backup
  .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.get_backup_policy
  .. automethod:: otcextensions.sdk.rds.v1._proxy.Proxy.set_backup_policy
