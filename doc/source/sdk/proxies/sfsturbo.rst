SFS Turbo API
=============

.. automodule:: otcextensions.sdk.sfsturbo.v1._proxy

The Shared File System Turbo Class
----------------------------------

The SFS Turbo high-level interface is available through the ``sfsturbo``
member of a :class:`~openstack.connection.Connection` object.  The
``sfsturbo`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Share Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sfsturbo.v1._proxy.Proxy
  :noindex:
  :members: shares, get_share, delete_share, find_share, extend_capacity,
            change_security_group
