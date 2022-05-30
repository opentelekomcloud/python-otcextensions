Database RDS API
================

For details on how to use database, see /sdk/guides/rds (NEEDS TO BE DONE)

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
  :noindex:
  :members: datastores, datastore_types

Flavor Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy
  :noindex:
  :members: flavors

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy
  :noindex:
  :members: instances, get_instance, find_instance,
            create_instance, delete_instance, restore_instance,
            get_instance_restore_time, restart_instance,
            enlarge_instance_volume, change_instance_flavor,
            get_instance_logs, add_tag, remove_tag


Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy
  :noindex:
  :members: backups, find_backup, create_backup, delete_backup,
            backup_download_links, get_instance_backup_policy,
            set_instance_backup_policy, wait_for_backup

Configuration Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v3._proxy.Proxy
  :noindex:
  :members: configurations, get_configuration, find_configuration,
            create_configuration, delete_configuration, update_configuration,
            apply_configuration
