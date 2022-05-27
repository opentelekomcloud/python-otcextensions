CSS API
=======

.. automodule:: otcextensions.sdk.css.v1._proxy

The Cloud Search Service Class
------------------------------

The css high-level interface is available through the ``css``
member of a :class:`~openstack.connection.Connection` object.  The
``css`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Cluster Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.css.v1._proxy.Proxy
  :noindex:
  :members: clusters, find_cluster, get_cluster, create_cluster,
            restart_cluster, extend_cluster, delete_cluster

Cluster Snapshot Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.css.v1._proxy.Proxy
  :noindex:
  :members: snapshots, create_snapshot, get_snapshot_policy, set_snapshot_policy,
            set_snapshot_configuration, disable_snapshot_function,
            restore_snapshot, delete_snapshot
