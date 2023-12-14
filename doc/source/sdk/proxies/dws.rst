DWS API
=======

.. automodule:: otcextensions.sdk.dws.v1._proxy

The Data Warehouse Service Class
--------------------------------

The dws high-level interface is available through the ``dws``
member of a :class:`~openstack.connection.Connection` object.  The
``dws`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Cluster Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dws.v1._proxy.Proxy
  :noindex:
  :members: clusters, find_cluster, get_cluster, create_cluster,
            restart_cluster, scale_out_cluster, reset_password,
            delete_cluster, list_cluster_tags, create_cluster_tag,
            delete_cluster_tag, batch_create_cluster_tags,
            batch_delete_cluster_tags

Cluster Snapshot Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dws.v1._proxy.Proxy
  :noindex:
  :members: snapshots, find_snapshot, get_snapshot, create_snapshot, create_snapshot,
            restore_snapshot, delete_snapshot

Cluster Flavor Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dws.v1._proxy.Proxy
  :noindex:
  :members: flavors
