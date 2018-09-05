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

   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.zones
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.create_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.get_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.delete_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.update_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.find_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.add_router_to_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.remove_router_from_zone
   .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.nameservers

Recordset Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dns.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.recordsets
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.create_recordset
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.get_recordset
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.update_recordset
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.delete_recordset


PTR Records Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dns.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.ptrs
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.create_ptr
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.get_ptr
  .. automethod:: otcextensions.sdk.dns.v2._proxy.Proxy.restore_ptr
