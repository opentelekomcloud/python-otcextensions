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

   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.hosts
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.create_host
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.get_host
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.find_host
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.delete_host
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.update_host
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.servers
   .. automethod:: otcextensions.sdk.deh.v1._proxy.Proxy.host_types
