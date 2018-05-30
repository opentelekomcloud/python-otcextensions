VolumeBackup API
================

For details on how to use auto scaling, see :doc:`/user/guides/volume_backup`

.. automodule:: otcextensions.sdk.volume_backup.v2._proxy

The VolumeBackup Class
----------------------

The VBS high-level interface is available through the ``volume_backup``
member of a :class:`~openstack.connection.Connection` object.  The
``volume_backup`` member will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.volume_backup.v2._proxy.Proxy

   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.backups
   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.get_backup
   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.create_backup
   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.delete_backup
   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.restore_backup
   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.wait_for_backup
   .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.wait_for_backup_delete

Backup Policy Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.volume_backup.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.backup_policies
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.create_backup_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.update_backup_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.delete_backup_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.find_backup_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.execute_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.enable_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.disable_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.link_resources_to_policy
  .. automethod:: otcextensions.sdk.volume_backup.v2._proxy.Proxy.unlink_resources_of_policy
