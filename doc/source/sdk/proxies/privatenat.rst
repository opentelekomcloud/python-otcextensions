Private NAT API
===============

.. automodule:: otcextensions.sdk.natv3.v3._proxy

The Private NAT high-level interface
------------------------------------

The private NAT high-level interface is available through the ``natv3``
member of a :class:`~openstack.connection.Connection` object. The
``natv3`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Private NAT Gateway Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.natv3.v3._proxy.Proxy
  :noindex:
  :members: private_nat_gateways, get_private_nat_gateway, private_dnat_rules, create_private_dnat_rule, update_private_dnat_rule, delete_private_dnat_rule, private_snat_rules, create_private_snat_rule, update_private_snat_rule, delete_private_snat_rule
