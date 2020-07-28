DeH API
=======

.. automodule:: otcextensions.sdk.deh.v1._proxy

The Dedicated Host Service Class
--------------------------------

The dehs high-level interface is available through the ``deh`` member of a
:class:`~openstack.connection.Connection` object.  The ``deh`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Host Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.deh.v1._proxy.Proxy
  :noindex:
  :members: hosts, get_host, find_host, create_host,
            update_host, delete_host, servers, host_types
