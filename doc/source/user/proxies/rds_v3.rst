Database RDS API
================

For details on how to use database, see :doc:`/user/guides/rds`

.. automodule:: otcextensions.sdk.rds.v3._proxy

The Database Class
------------------

The database high-level interface is available through the ``rds`` member of a
:class:`~openstack.connection.Connection` object.  The ``rds`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Datastore Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.datastore_types
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.datastores

Flavor Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.flavors

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.create_instance
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.delete_instance
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.get_instance
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.find_instance
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.instances
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.restore_instance
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.get_instance_restore_time

Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.backups
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.create_backup
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.delete_backup
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.find_backup
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.backup_download_links
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.get_instance_backup_policy
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.set_instance_backup_policy
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.wait_for_backup

Configuration Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy

   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.configurations
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.get_configuration
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.find_configuration
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.create_configuration
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.delete_configuration
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.update_configuration
   .. automethod:: otcextensions.sdk.rds.v3._proxy.Proxy.apply_configuration
