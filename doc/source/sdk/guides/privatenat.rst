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

List Private NAT Gateways
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query Private NAT gateway list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.natv3.v3.gateway.Gateway`.

.. literalinclude:: ../examples/natv3/list_private_gateways.py
   :lines: 16-23

Get Private NAT Gateway
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get a Private NAT gateway by ID
:class:`~otcextensions.sdk.natv3.v3.gateway.Gateway`.

.. literalinclude:: ../examples/natv3/get_private_gateway.py
   :lines: 16-24

Create Private NAT Gateway
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a Private NAT gateway
:class:`~otcextensions.sdk.natv3.v3.gateway.Gateway`.

.. literalinclude:: ../examples/natv3/create_private_gateway.py
   :lines: 16-35

Delete Private NAT Gateway
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete the Private NAT gateway
:class:`~otcextensions.sdk.natv3.v3.gateway.Gateway`.

.. literalinclude:: ../examples/natv3/delete_private_gateway.py
   :lines: 16-24

Update Private NAT Gateway
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a Private NAT gateway
:class:`~otcextensions.sdk.natv3.v3.gateway.Gateway`.

.. literalinclude:: ../examples/natv3/update_private_gateway.py
   :lines: 16-27

DNAT
----

The DNAT function enables servers that share the same EIPs in
a VPC to provide services accessible from the Internet through
the IP address mapping and port mapping.

List Private DNAT Rules
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query a DNAT rule list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`.

.. literalinclude:: ../examples/natv3/list_private_dnat_rules.py
   :lines: 16-23

Create Private DNAT Rules
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a DNAT rule.
:class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`.

.. literalinclude:: ../examples/natv3/create_private_dnat_rules.py
   :lines: 16-32

Get Private DNAT Rule
^^^^^^^^^^^^^^^^^^^^^

This interface is used to query details about a specified DNAT rule.
:class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`.

.. literalinclude:: ../examples/natv3/get_private_dnat_rule.py
   :lines: 16-22

Update Private DNAT Rule
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a specified DNAT rule.
:class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`.

.. literalinclude:: ../examples/natv3/update_private_dnat_rule.py
   :lines: 16-22

Delete Private DNAT Rule
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a specified DNAT rule.
:class:`~otcextensions.sdk.natv3.v3.dnat.PrivateDnat`.

.. literalinclude:: ../examples/natv3/delete_private_dnat_rule.py
   :lines: 16-22

SNAT
----

The SNAT function enables servers in a VPC or connected networks to use
transit IP addresses for outbound private address translation.

List Private SNAT Rules
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query an SNAT rule list and to filter
the output with query parameters.
:class:`~otcextensions.sdk.natv3.v3.snat.PrivateSnat`.

.. literalinclude:: ../examples/natv3/list_private_snat_rules.py
   :lines: 16-23

Get Private SNAT Rule
^^^^^^^^^^^^^^^^^^^^^

This interface is used to query details about a specified SNAT rule.
:class:`~otcextensions.sdk.natv3.v3.snat.PrivateSnat`.

.. literalinclude:: ../examples/natv3/get_private_snat_rule.py
   :lines: 16-22

Create Private SNAT Rule
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create an SNAT rule.
:class:`~otcextensions.sdk.natv3.v3.snat.PrivateSnat`.

.. literalinclude:: ../examples/natv3/create_private_snat_rule.py
   :lines: 16-28

Update Private SNAT Rule
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a specified SNAT rule.
:class:`~otcextensions.sdk.natv3.v3.snat.PrivateSnat`.

.. literalinclude:: ../examples/natv3/update_private_snat_rule.py
   :lines: 16-24

Delete Private SNAT Rule
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a specified SNAT rule.
:class:`~otcextensions.sdk.natv3.v3.snat.PrivateSnat`.

.. literalinclude:: ../examples/natv3/delete_private_snat_rule.py
   :lines: 16-22

Transit IP Addresses
--------------------

Transit IP addresses are used by private NAT gateways for private network
address translation.

List Private Transit IP Addresses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query transit IP addresses and to filter
the output with query parameters.
:class:`~otcextensions.sdk.natv3.v3.transit_ip.PrivateTransitIp`.

.. literalinclude:: ../examples/natv3/list_private_transit_ips.py
   :lines: 16-23
