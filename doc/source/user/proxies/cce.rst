CCE API
=======

.. automodule:: otcextensions.sdk.cce.v1._proxy

The Cloud Container Engine Class
--------------------------------

The cce high-level interface is available through the ``cce``
member of a :class:`~openstack.connection.Connection` object.  The
``cce`` member will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Cluster Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cce.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.cce.v1._proxy.Proxy.clusters
   .. automethod:: otcextensions.sdk.cce.v1._proxy.Proxy.get_cluster
   .. automethod:: otcextensions.sdk.cce.v1._proxy.Proxy.delete_cluster
   .. automethod:: otcextensions.sdk.cce.v1._proxy.Proxy.delete_cluster_nodes
   .. automethod:: otcextensions.sdk.cce.v1._proxy.Proxy.add_node
