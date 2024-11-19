VPCEP API
=========

.. automodule:: otcextensions.sdk.vpcep.v1._proxy

The VPC Endpoint Class
----------------------

The vpcep high-level interface is available through the ``vpcep``
member of a :class:`~openstack.connection.Connection` object.  The
``vpcep`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Endpoint Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: endpoints, create_endpoint, get_endpoint, delete_endpoint

Service Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: services, create_service, get_service, find_service, delete_service

Service Connection Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: service_connections, manage_service_connections

Service WhiteList Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: service_whitelist, manage_service_whitelist

Public Service Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: public_services

Target Service Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: get_target_service

Quota Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vpcep.v1._proxy.Proxy
  :noindex:
  :members: resource_quota
