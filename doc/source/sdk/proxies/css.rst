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
            restart_cluster, extend_cluster, extend_cluster_nodes,
            delete_cluster, update_cluster_name, update_cluster_password,
            update_cluster_flavor, update_cluster_security_mode,
            update_cluster_security_group, update_cluster_kernel,
            get_cluster_version_upgrade_info, scale_in_cluster,
            scale_in_cluster_by_node_type, replace_cluster_node,
            add_cluster_nodes, get_cluster_upgrade_info,
            retry_cluster_upgrade_job, retry_cluster_upgrade_job


Cluster Snapshot Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.css.v1._proxy.Proxy
  :noindex:
  :members: snapshots, find_snapshot, create_snapshot, get_snapshot_policy,
            set_snapshot_policy, set_snapshot_configuration,
            disable_snapshot_function, restore_snapshot, delete_snapshot
