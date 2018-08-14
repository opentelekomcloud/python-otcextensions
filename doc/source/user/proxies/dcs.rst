DCS API
=======

.. automodule:: otcextensions.sdk.dcs.v1._proxy

The Distributed Message Service Class
-------------------------------------

The dcs high-level interface is available through the ``dcs``
member of a :class:`~openstack.connection.Connection` object.  The
``dcs`` member will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcs.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.instances
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.create_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.get_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.find_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.delete_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.update_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.extend_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.start_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.restart_instance
   .. automethod:: otcextensions.sdk.dcs.v1._proxy.Proxy.stop_instance
