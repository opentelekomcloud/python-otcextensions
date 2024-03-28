VPC Endpoint (VPCEP)
====================

VPC Endpoint (VPCEP) is a cloud service that provides secure and
private channels to connect your VPCs to VPC endpoint services,
including cloud services or your private services. It allows you
to plan networks flexibly without having to use EIPs. There are two
types of resources: VPC endpoint services and VPC endpoints.

.. contents:: Table of Contents
   :local:

VPC Endpoint Service
--------------------

VPC endpoint services are cloud services or private services that
you manually configure in VPCEP. You can access these endpoint
services using VPC endpoints.

List Services
^^^^^^^^^^^^^

This interface is used to query an VPCEP services list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.vpcep.v2.service.Service`.

.. literalinclude:: ../examples/vpcep/list_endpoints.py
   :lines: 14-20

Create Service
^^^^^^^^^^^^^^

This interface is used to create a VPCEP service with
parameters.
:class:`~otcextensions.sdk.vpcep.v2.service.Service`.

.. literalinclude:: ../examples/vpcep/create_service.py
   :lines: 14-30

Get Service
^^^^^^^^^^^

This interface is used to get a VPCEP service by ID
or an instance of class.
:class:`~otcextensions.sdk.vpcep.v2.service.Service`.

.. literalinclude:: ../examples/vpcep/get_service.py
   :lines: 14-21

Find Service
^^^^^^^^^^^^

This interface is used to find a VPCEP service by ID
or name.
:class:`~otcextensions.sdk.vpcep.v2.service.Service`.

.. literalinclude:: ../examples/vpcep/find_service.py
   :lines: 14-21

Delete Service
^^^^^^^^^^^^^^

This interface is used to delete a VPCEP service by ID
or an instance of class
:class:`~otcextensions.sdk.vpcep.v2.service.Service`.

.. literalinclude:: ../examples/vpcep/delete_service.py
   :lines: 14-20

List Service Whitelist
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query an VPCEP service whitelist and to filter
the output with query parameters.
:class:`~otcextensions.sdk.vpcep.v2.whitelist.Whitelist`.

.. literalinclude:: ../examples/vpcep/list_service_whitelist.py
   :lines: 14-22

Manage Service Whitelist
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to manage a VPCEP service whitelist.
:class:`~otcextensions.sdk.vpcep.v2.whitelist.Whitelist`.

.. literalinclude:: ../examples/vpcep/manage_service_whitelist.py
   :lines: 14-27

List Service Connections
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query an VPCEP service connections and to filter
the output with query parameters.
:class:`~otcextensions.sdk.vpcep.v2.connection.Connection`.

.. literalinclude:: ../examples/vpcep/list_service_connections.py
   :lines: 14-22

Manage Service Connections
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to manage a VPCEP service connections.
:class:`~otcextensions.sdk.vpcep.v2.connection.Connection`.

.. literalinclude:: ../examples/vpcep/manage_service_connections.py
   :lines: 14-27

VPC Endpoint
------------

VPC endpoints are secure and private channels for connecting
VPCs to VPC endpoint services.

List Endpoints
^^^^^^^^^^^^^^

This interface is used to query an VPC endpoint list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.vpcep.v2.endpoint.Endpoint`.

.. literalinclude:: ../examples/vpcep/list_endpoints.py
   :lines: 14-20

Create Endpoint
^^^^^^^^^^^^^^^

This interface is used to create a VPC endpoint with
parameters.
:class:`~otcextensions.sdk.vpcep.v2.endpoint.Endpoint`.

.. literalinclude:: ../examples/vpcep/create_endpoint.py
   :lines: 14-28

Get Endpoint
^^^^^^^^^^^^

This interface is used to get a VPC endpoint by ID
or an instance of class
:class:`~otcextensions.sdk.vpcep.v2.endpoint.Endpoint`.

.. literalinclude:: ../examples/vpcep/get_endpoint.py
   :lines: 14-21

Delete Endpoint
^^^^^^^^^^^^^^^

This interface is used to delete a VPC endpoint by ID
or an instance of class
:class:`~otcextensions.sdk.vpcep.v2.endpoint.Endpoint`.

.. literalinclude:: ../examples/vpcep/delete_endpoint.py
   :lines: 14-20

VPCEP Quota
-----------

List Resource Quota
^^^^^^^^^^^^^^^^^^^

This interface is used to query quota of vpc endpoint and endpoint_service
on a specific tenant.
:class:`~otcextensions.sdk.vpcep.v2.quota.Quota`.

.. literalinclude:: ../examples/vpcep/list_resource_quota.py
   :lines: 14-20

