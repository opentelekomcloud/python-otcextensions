Direct Connect (DCAAS)
======================

.. contents:: Table of Contents
   :local:

Virtual Gateway
---------------

Virtual gateways function as virtual routers, linking direct connections
to VPCs. A virtual gateway is bound to the VPC that is directly connected
to a cloud private line. You can use the virtual gateway to connect to the
network segment of the VPC to be accessed, and then use the VPC peering
connections to access multiple VPCs.

List Virtual Gateways
^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all virtual gateways accessible to
the tenant submitting the request. The virtual gateways are filtered based on
the filtering condition.
:class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`.

.. literalinclude:: ../examples/dcaas/list_virtual_gateways.py
   :lines: 16-25

Create Virtual Gateway
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a virtual gateway with parameters.
:class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`.

.. literalinclude:: ../examples/dcaas/create_virtual_gateway.py
   :lines: 16-29

Get Virtual Gateway
^^^^^^^^^^^^^^^^^^^

This interface is used to get a virtual gateway by ID
or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`.

.. literalinclude:: ../examples/dcaas/get_virtual_gateway.py
   :lines: 16-28

Find Virtual Gateway
^^^^^^^^^^^^^^^^^^^^

This interface is used to find a virtual gateway by id or name.
:class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`.

.. literalinclude:: ../examples/dcaas/find_virtual_gateway.py
   :lines: 16-28

Update Virtual Gateway
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update parameters of a virtual gateway by
id or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`.

.. literalinclude:: ../examples/dcaas/update_virtual_gateway.py
   :lines: 16-29

Delete Virtual Gateway
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a virtual gateway by ID
or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.virtual_gateway.VirtualGateway`.

.. literalinclude:: ../examples/dcaas/delete_virtual_gateway.py
   :lines: 16-24

Connection
----------

Connections are abstractions of network circuits between locations on the
cloud and local data centers. We provide ports only. After creating
a connection, you need to contact the carrier to perform offline construction
and set up the physical line for you. Connections are dedicated channels for
your local data centers to access VPCs on the cloud. Compared with the
traditional public network, connections are more stable, reliable, and secure.
They provide a maximum transmission rate of 10 Gbit/s.

List Connections
^^^^^^^^^^^^^^^^

This interface is used to query all connections accessible to
the tenant submitting the request. The connection are filtered based on
the filtering condition.
:class:`~otcextensions.sdk.dcaas.v2.connection.Connection`.

.. literalinclude:: ../examples/dcaas/list_connections.py
   :lines: 16-25

Create Connection
^^^^^^^^^^^^^^^^^

This interface is used to create a connection with parameters.
:class:`~otcextensions.sdk.dcaas.v2.connection.Connection`.

.. literalinclude:: ../examples/dcaas/create_connection.py
   :lines: 16-29

Get Connection
^^^^^^^^^^^^^^

This interface is used to get a connection by ID or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.connection.Connection`.

.. literalinclude:: ../examples/dcaas/get_connection.py
   :lines: 16-28

Find Connection
^^^^^^^^^^^^^^^

This interface is used to find a connection by id or name.
:class:`~otcextensions.sdk.dcaas.v2.connection.Connection`.

.. literalinclude:: ../examples/dcaas/find_connection.py
   :lines: 16-28

Update Connection
^^^^^^^^^^^^^^^^^

This interface is used to update parameters of a connection by id or an
instance of class.
:class:`~otcextensions.sdk.dcaas.v2.connection.Connection`.

.. literalinclude:: ../examples/dcaas/update_connection.py
   :lines: 16-29

Delete Connection
^^^^^^^^^^^^^^^^^

This interface is used to delete a connection by ID or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.connection.Connection`.

.. literalinclude:: ../examples/dcaas/delete_connection.py
   :lines: 16-24

Virtual Interface
-----------------

Virtual interfaces associate user gateways with virtual gateways, enabling
local data centers to access VPCs.

List Virtual Interfaces
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all virtual interfaces accessible to
the tenant submitting the request. The virtual interfaces are filtered based on
the filtering condition.
:class:`~otcextensions.sdk.dcaas.v2.virtual_interface.VirtualInterface`.

.. literalinclude:: ../examples/dcaas/list_virtual_interfaces.py
   :lines: 16-25

Create Virtual Interface
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a virtual interface with parameters.
:class:`~otcextensions.sdk.dcaas.v2.virtual_interface.VirtualInterface`.

.. literalinclude:: ../examples/dcaas/create_virtual_interface.py
   :lines: 16-29

Get Virtual Interface
^^^^^^^^^^^^^^^^^^^^^

This interface is used to get a virtual interface by ID
or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.virtual_interface.VirtualInterface`.

.. literalinclude:: ../examples/dcaas/get_virtual_interface.py
   :lines: 16-28

Find Virtual Interface
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to find a virtual interface by id or name.
:class:`~otcextensions.sdk.dcaas.v2.virtual_interface.VirtualInterface`.

.. literalinclude:: ../examples/dcaas/find_virtual_interface.py
   :lines: 16-28

Update Virtual Interface
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update parameters of a virtual interface by
id or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.virtual_interface.VirtualInterface`.

.. literalinclude:: ../examples/dcaas/update_virtual_interface.py
   :lines: 16-29

Delete Virtual Interface
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a virtual interface by ID
or an instance of class.
:class:`~otcextensions.sdk.dcaas.v2.virtual_interface.VirtualInterface`.

.. literalinclude:: ../examples/dcaas/delete_virtual_interface.py
   :lines: 16-24

Endpoint Group
--------------

List Endpoint Groups
^^^^^^^^^^^^^^^^^^^^

This interface is used to query the Direct Connect Endpoint Group list and
to filter the output with query parameters.

.. literalinclude:: ../examples/dcaas/list_endpoint_groups.py
   :lines: 16-26

Create Endpoint Group
^^^^^^^^^^^^^^^^^^^^^

This interface is used to create Direct Connect Endpoint Group with parameters.

.. literalinclude:: ../examples/dcaas/create_endpoint_group.py
   :lines: 16-32

Get Endpoint Group
^^^^^^^^^^^^^^^^^^

This interface is used to get a DCAAS Endpoint Group by ID
or an instance of class
:class:`~otcextensions.sdk.dcaas.v2.endpoint_group.DirectConnectEndpointGroup`.

.. literalinclude:: ../examples/dcaas/get_endpoint_group.py
   :lines: 16-28

Find Endpoint Group
^^^^^^^^^^^^^^^^^^^

This interface is used to find a Direct Connect Endpoint Group by name or ID.

.. literalinclude:: ../examples/dcaas/find_endpoint_group.py
   :lines: 16-28

Update Endpoint Group
^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a Direct Connect Endpoint Group by ID
or an instance of class
:class:`~otcextensions.sdk.dcaas.v2.endpoint_group.DirectConnectEndpointGroup`.

.. literalinclude:: ../examples/dcaas/update_endpoint_group.py
   :lines: 16-29

Delete Endpoint Group
^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a Direct Connect Endpoint Group by ID
or an instance of class
:class:`~otcextensions.sdk.dcaas.v2.endpoint_group.DirectConnectEndpointGroup`.

.. literalinclude:: ../examples/dcaas/delete_endpoint_group.py
   :lines: 16-24
