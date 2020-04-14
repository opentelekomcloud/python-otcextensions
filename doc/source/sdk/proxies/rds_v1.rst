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
  :noindex:
  :members: datastore_versions, get_datastore_version, datastore_types

Flavor Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy
  :noindex:
  :members: flavors, get_flavor

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy
  :noindex:
  :members: instances, get_instance, find_instance,
            create_instance, delete_instance, update_instance

Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.rds.v1._proxy.Proxy
  :noindex:
  :members: backups, create_backup, delete_backup,
            get_backup_policy, set_backup_policy
