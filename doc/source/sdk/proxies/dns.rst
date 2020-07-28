DNS API
=======

.. automodule:: otcextensions.sdk.dns.v2._proxy

The DNS Service Class
---------------------

The dns high-level interface is available through the ``dns``
member of a :class:`~openstack.connection.Connection` object.  The
``dns`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Zone Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dns.v2._proxy.Proxy
  :noindex:
  :members: zones, create_zone, get_zone, delete_zone,
            update_zone, find_zone, add_router_to_zone,
            remove_router_from_zone, nameservers

Recordset Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dns.v2._proxy.Proxy
  :noindex:
  :members: recordsets, create_recordset, get_recordset, update_recordset,
            delete_recordset


PTR Records Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dns.v2._proxy.Proxy
  :noindex:
  :members: floating_ips, set_floating_ip, get_floating_ip, unset_floating_ip
