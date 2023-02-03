Virtual Private Cloud (VPC)
===========================

.. contents:: Table of Contents
   :local:

VPC Bandwidth
--------------

Shared bandwidth allows multiple EIPs to share the same bandwidth.
All ECSs, BMSs, and load balancers that have EIPs bound in the same region
can share a bandwidth.

Assign bandwidth
^^^^^^^^^^^^^^^^^

This interface is used to assign a shared bandwidth.
:class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`.

.. literalinclude:: ../examples/vpc/assign_bandwidth.py
   :lines: 16-23

Add eip to bandwidth
^^^^^^^^^^^^^^^^^^^^^

This interface is used to add an EIP to a shared bandwidth.
:class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`.

.. literalinclude:: ../examples/vpc/add_eip_to_bandwidth.py
   :lines: 16-25

Remove eip from bandwidth
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to remove an EIP from a shared bandwidth.
:class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`.

.. literalinclude:: ../examples/vpc/remove_eip_from_bandwidth.py
   :lines: 16-27

Delete bandwidth
^^^^^^^^^^^^^^^^

This interface is used to delete a shared bandwidth.
:class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`.

.. literalinclude:: ../examples/vpc/delete_bandwidth.py
   :lines: 16-22

VPC Peering Connection
----------------------

A VPC peering connection is a network connection between two VPCs that
enables you to route traffic between them using private IP addresses.
ECSs in either VPC can communicate with each other just as if they were in
the same VPC. You can create a VPC peering connection between your own VPCs,
or between your VPC and another account's VPC within the same region. A VPC
peering connection between VPCs in different regions will not take effect.

List VPC Peerings
^^^^^^^^^^^^^^^^^

This interface is used to query all VPC peering connections accessible to the
tenant submitting the request. The connections are filtered based on the
filtering condition.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/list_peerings.py
   :lines: 16-23

Create VPC Peering
^^^^^^^^^^^^^^^^^^

This interface is used to create a VPC peering connection  with
parameters.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/create_peering.py
   :lines: 16-33

Get VPC Peering
^^^^^^^^^^^^^^^

This interface is used to get a VPC peering connection by ID
or an instance of class.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/get_peering.py
   :lines: 16-26

Find VPC Peering
^^^^^^^^^^^^^^^^

This interface is used to find a VPC peering connection by id or name.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/find_peering.py
   :lines: 16-26

Update VPC Peering
^^^^^^^^^^^^^^^^^^

This interface is used to update parameters of a VPC peering connection by
id or an instance of class.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/update_peering.py
   :lines: 16-24

Delete VPC Peering
^^^^^^^^^^^^^^^^^^

This interface is used to delete a VPC peering connection by ID
or an instance of class.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/delete_peering.py
   :lines: 16-23

Set VPC Peering
^^^^^^^^^^^^^^^

This interface is used to accept of reject a VPC peering connection
request by ID or an instance of class.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/set_peering.py
   :lines: 16-32


VPC Route
---------

To enable communication between the two VPCs, you need to add local and
peer routes for the VPC peering connection.

List VPC Routes
^^^^^^^^^^^^^^^

This interface is used to query all routes of the tenant submitting the
request. The routes are filtered based on the filtering condition.
:class:`~otcextensions.sdk.vpc.v1.route.Route`.

.. literalinclude:: ../examples/vpc/list_routes.py
   :lines: 16-23

Add VPC Route
^^^^^^^^^^^^^

This Interface is used to add a VPC route.
:class:`~otcextensions.sdk.vpc.v1.route.Route`.

.. literalinclude:: ../examples/vpc/add_route.py
   :lines: 16-31

Get VPC Route
^^^^^^^^^^^^^

This interface is used to get a VPC route by ID
or an instance of class.
:class:`~otcextensions.sdk.vpc.v1.route.Route`.

.. literalinclude:: ../examples/vpc/get_route.py
   :lines: 16-26

Delete VPC Route
^^^^^^^^^^^^^^^^

This interface is used to delete a VPC route by ID
or an instance of class.
:class:`~otcextensions.sdk.vpc.v1.peering.Peering`.

.. literalinclude:: ../examples/vpc/delete_route.py
   :lines: 16-23
