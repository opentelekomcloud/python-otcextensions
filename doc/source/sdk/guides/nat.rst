Network Address Translation (NAT)
=================================

.. contents:: Table of Contents
   :local:

NAT Gateway
-----------

The NAT Gateway service provides the network address translation (NAT)
function for servers, such as Elastic Cloud Servers (ECSs), Bare Metal
Servers (BMSs), and Workspace desktops, in a Virtual Private Cloud (VPC)
or servers that connect to a VPC through Direct Connect or Virtual
Private Network (VPN) in local data centers, allowing these servers to
share elastic IP addresses (EIPs) to access the Internet or to provide
services accessible from the Internet.

List NAT Gateways
^^^^^^^^^^^^^^^^^

This interface is used to query an NAT gateway list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.nat.v2.gateway.Gateway`.

.. literalinclude:: ../examples/nat/list_gateways.py
   :lines: 16-23

Create NAT Gateway
^^^^^^^^^^^^^^^^^^

This interface is used to create a NAT Ggateway with
parameters.
:class:`~otcextensions.sdk.nat.v2.gateway.Gateway`.

.. literalinclude:: ../examples/nat/create_gateway.py
   :lines: 16-31

Get NAT Gateway
^^^^^^^^^^^^^^^

This interface is used to get a NAT gateway by ID
or an instance of class
:class:`~otcextensions.sdk.nat.v2.gateway.Gateway`.

.. literalinclude:: ../examples/nat/get_gateway.py
   :lines: 16-23

Find NAT Gateway
^^^^^^^^^^^^^^^^

This interface is used to find a NAT gateway by id or name.
:class:`~otcextensions.sdk.nat.v2.gateway.Gateway`.

.. literalinclude:: ../examples/nat/find_gateway.py
   :lines: 16-24

Update NAT Gateway
^^^^^^^^^^^^^^^^^^

This interface is used to update NAT gateway parameters by
id or an instance of class
:class:`~otcextensions.sdk.nat.v2.gateway.Gateway`.

.. literalinclude:: ../examples/nat/update_gateway.py
   :lines: 16-31

Delete NAT Gateway
^^^^^^^^^^^^^^^^^^

This interface is used to delete a NAT gateway by ID
or an instance of class
:class:`~otcextensions.sdk.nat.v2.gateway.Gateway`.

.. literalinclude:: ../examples/nat/delete_gateway.py
   :lines: 16-24

NAT Gateway supports source NAT (SNAT) and destination NAT (DNAT)
functions.

SNAT
----

The SNAT function translates a private IP address to a public IP
address by binding EIPs to servers in a VPC, providing secure and
efficient access to the Internet.

List SNAT Rules
^^^^^^^^^^^^^^^

This interface is used to query an SNAT rule list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.nat.v2.snat.Snat`.

.. literalinclude:: ../examples/nat/list_snat_rules.py
   :lines: 16-23

Create SNAT Rule
^^^^^^^^^^^^^^^^

This interface is used to create a SNAT rule with
parameters.
:class:`~otcextensions.sdk.nat.v2.snat.Snat`.

.. literalinclude:: ../examples/nat/create_snat_rule.py
   :lines: 16-33

Get SNAT Rule
^^^^^^^^^^^^^

This interface is used to get a SNAT rule by ID
or an instance of class
:class:`~otcextensions.sdk.nat.v2.snat.Snat`.

.. literalinclude:: ../examples/nat/get_snat_rule.py
   :lines: 16-24

Delete SNAT Rule
^^^^^^^^^^^^^^^^

This interface is used to delete a SNAT Rule by ID
or an instance of class
:class:`~otcextensions.sdk.nat.v2.snat.Snat`.

.. literalinclude:: ../examples/nat/delete_snat_rule.py
   :lines: 16-23


DNAT
----

The DNAT function enables servers that share the same EIPs in
a VPC to provide services accessible from the Internet through
the IP address mapping and port mapping.

List DNAT Rules
^^^^^^^^^^^^^^^

This interface is used to query an DNAT rule list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.nat.v2.dnat.Dnat`.

.. literalinclude:: ../examples/nat/list_dnat_rules.py
   :lines: 16-23

Create DNAT Rule
^^^^^^^^^^^^^^^^

This interface is used to create a DNAT rule with
parameters.
:class:`~otcextensions.sdk.nat.v2.dnat.Dnat`.

.. literalinclude:: ../examples/nat/create_dnat_rule.py
   :lines: 16-42

Get DNAT Rule
^^^^^^^^^^^^^

This interface is used to get a DNAT rule by ID
or an instance of class
:class:`~otcextensions.sdk.nat.v2.dnat.Dnat`.

.. literalinclude:: ../examples/nat/get_dnat_rule.py
   :lines: 16-24

Delete DNAT Rule
^^^^^^^^^^^^^^^^

This interface is used to delete a DNAT Rule by ID
or an instance of class
:class:`~otcextensions.sdk.nat.v2.dnat.Dnat`.

.. literalinclude:: ../examples/nat/delete_snat_rule.py
   :lines: 16-23

