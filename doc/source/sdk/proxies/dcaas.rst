DCAAS API
=========

.. automodule:: otcextensions.sdk.dcaas.v2._proxy

The Direct Connect Class
-------------------------------

The direct connect high-level interface is available through the ``dcaas``
member of a :class:`~openstack.connection.Connection` object.  The
``dcaas`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

DCAAS Virtual Gateway
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcaas.v2._proxy.Proxy
  :noindex:
  :members: virtual_gateways, find_virtual_gateway, create_virtual_gateway,
            update_virtual_gateway, delete_virtual_gateway, get_virtual_gateway

DCAAS Connection
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcaas.v2._proxy.Proxy
  :noindex:
  :members: connections, find_connection, create_connection,
            update_connection, delete_connection, get_connection
