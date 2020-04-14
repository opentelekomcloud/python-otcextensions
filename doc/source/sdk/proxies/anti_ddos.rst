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
  :noindex:
  :members: floating_ips, protect_floating_ip, unprotect_floating_ip,
            get_floating_ip_policies, update_floating_ip_policies,
            get_floating_ip_status, floating_ip_events, floating_ip_stat_day,
            floating_ip_stat_week

Misc Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.anti_ddos.v1._proxy.Proxy
  :noindex:
  :members: configs
