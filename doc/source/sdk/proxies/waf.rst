Web Application Firewall API
============================

.. automodule:: otcextensions.sdk.waf.v1._proxy

The WAF Service Class
---------------------

The waf high-level interface is available through the ``waf``
member of a :class:`~openstack.connection.Connection` object.  The
``waf`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Certificate Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.waf.v1._proxy.Proxy
  :noindex:
  :members: certificates, create_certificate, get_certificate,
            delete_certificate, update_certificate, find_certificate


