VolumeBackup API
================

For details on how to use auto scaling, see /sdk/guides/volume_backup
(NEEDS TO BE DONE).

.. automodule:: otcextensions.sdk.volume_backup.v2._proxy

The VolumeBackup Class
----------------------

The VBS high-level interface is available through the
``volume_backup`` member of a
:class:`~openstack.connection.Connection` object.  The
``volume_backup`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

The Backup itself is an OpenStack entity and supported natively as
block_storage.Backup.


Backup Policy Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.volume_backup.v2._proxy.Proxy
  :noindex:
  :members: backup_policies, find_backup_policy, create_backup_policy,
            update_backup_policy, delete_backup_policy, execute_policy,
            enable_policy, disable_policy, link_resources_to_policy,
            unlink_resources_of_policy
