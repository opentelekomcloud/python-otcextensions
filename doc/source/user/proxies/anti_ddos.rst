Anti_DDoS API
=============

.. automodule:: otcextensions.sdk.anti_ddos.v1._proxy

The Anti DDoS Service Class
---------------------------

The anti_ddos high-level interface is available through the ``anti_ddos``
member of a :class:`~openstack.connection.Connection` object.  The
``anti_ddos`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Floating IP Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.floating_ips
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.protect_floating_ip
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.unprotect_floating_ip
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.get_floating_ip_policies
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.update_floating_ip_policies
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.get_floating_ip_status
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.floating_ip_events
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.floating_ip_stat_day
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.floating_ip_stat_week
   .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.update_floating_ip_policies

Misc Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy.configs
