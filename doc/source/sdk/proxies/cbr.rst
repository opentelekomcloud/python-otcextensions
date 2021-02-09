CBR API
=======

.. automodule:: otcextensions.sdk.cbr.v3._proxy

The Cloud Backup and Recovery Service Class
-------------------------------------------

The CBR high-level interface is available through the ``cbr``
member of a :class:`~openstack.connection.Connection` object.  The
``ces`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cbr.v3._proxy.Proxy
  :noindex:
  :members: backups, get_backup, delete_backup, find_backup

Restore Point (Checkpoint) Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cbr.v3._proxy.Proxy
  :noindex:
  :members: get_checkpoint, create_checkpoint

Restore Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cbr.v3._proxy.Proxy
  :noindex:
  :members: restore_data
