NAT API
=======

.. automodule:: otcextensions.sdk.natv3.v3._proxy

The Network Address Translation Class
-------------------------------------

The nat high-level interface is available through the ``natv3``
member of a :class:`~openstack.connection.Connection` object.  The
``natv3`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Gateway Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.nat.v2._proxy.Proxy
  :noindex:
  :members: gateways
