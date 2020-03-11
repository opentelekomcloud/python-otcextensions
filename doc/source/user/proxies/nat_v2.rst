Database NAT API
================

For details on how to use database, see :doc:`/user/guides/rds`

.. automodule:: otcextensions.sdk.nat.v2._proxy

The NAT Class
--------------

The NAT high-level interface is available through the ``nat`` member of a
:class:`~openstack.connection.Connection` object.  The ``nat`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

NAT Gateway Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy

   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.create_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.update_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.get_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.find_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.gateways


NAT Snat Rule Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.create_snat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_snat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.get_snat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_snat_rule


NAT Dnat Rule Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.create_dnat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_dnat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.get_dnat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_dnat_rule
