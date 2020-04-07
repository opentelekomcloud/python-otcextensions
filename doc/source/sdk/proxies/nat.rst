NAT API
=======

.. automodule:: otcextensions.sdk.nat.v2._proxy

The Network Address Translation Class
-------------------------------------

The nat high-level interface is available through the ``nat``
member of a :class:`~openstack.connection.Connection` object.  The
``nat`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Gateway Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy

   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.gateways
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.create_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.find_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.update_gateway
   .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_gateway


SNAT Rule Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.snat_rules
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.create_snat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.get_snat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_snat_rule


DNAT Rule Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy

  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.dnat_rules
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.create_dnat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.get_dnat_rule
  .. automethod:: otcextensions.sdk.nat.v2._proxy.Proxy.delete_dnat_rule
