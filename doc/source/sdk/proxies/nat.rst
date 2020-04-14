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
  :noindex:
  :members: gateways, find_gateway,
            create_gateway, update_gateway, delete_gateway

SNAT Rule Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy
  :noindex:
  :members: snat_rules, get_snat_rule, create_snat_rule, delete_snat_rule

DNAT Rule Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy
  :noindex:
  :members: dnat_rules, get_dnat_rule, create_dnat_rule, delete_dnat_rule
