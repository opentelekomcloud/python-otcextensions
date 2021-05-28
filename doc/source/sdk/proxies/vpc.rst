VPC API
=======

.. automodule:: otcextensions.sdk.vpc.v2._proxy

The Virtual Private Cloud Class
-------------------------------

The nat high-level interface is available through the ``vpc``
member of a :class:`~openstack.connection.Connection` object.  The
``vpc`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

VPC Peering Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpc.v2._proxy.Proxy
  :noindex:
  :members: peerings, find_peering, create_peering,
            update_peering, delete_peering, set_peering

VPC Route Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpc.v2._proxy.Proxy
  :noindex:
  :members: routes, get_route, add_route, delete_route
