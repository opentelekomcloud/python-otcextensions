Domain Name Service (DNS)
=========================

.. contents:: Table of Contents
   :local:

Domain Name Services (DNS) assign IP addresses to meaningful domain names
(such as www.telekom.de). These plain-text names are much easier to remember
than 12-digit numbers. Thanks to DNS resolution, users can access network
applications by entering the domain name. As such, the DNS also simplifies
work in public clouds. It enables users to integrate cloud resources in their
own company networks with ease – they then see the services as part of their
internal network. Moreover, using domain names instead of IP addresses also
facilitates administrative tasks and makes clouds more user-friendly.
The Open Telekom Cloud also offers a Domain Name Service (DNS). DNS is
available via the Open Telekom Cloud console and features anti-DDoS
protection. In addition to references to external IP addresses, the solution
can also be used for services within the Open Telekom Cloud. Pricing of the
Domain Name Service is based on scaled prices depending on the number of
domains stored. If a domain is created and remains configured for more than
24 hours, it is billed once for the entire month. A usage-based payment is
then added to this (domain requests).

Zone
----

There are private and public zones available.
A large number of DNS servers are available on the Internet, constituting DNS
domain namespaces. Each DNS server has its own domain name resolution
responsibilities. Only when a DNS server cannot resolve a domain name itself,
it forwards the request to another DNS server. Domain namespaces are managed
by segment. That is, a large space is divided into several separately hosted
zones. Each public zone is a part of the namespace that is administered by a
particular DNS server. For example, a DNS server is configured on the cloud
platform to resolve all domain names in the namespace example.com. Public
zones are accessible to hosts on the Internet.
A private zone is a namespace in which domain names are resolved by private
DNS servers It records the route for a domain name to be accessed in one
or more VPCs. Private zones are accessible only to hosts in specified VPCs.

List Zones
^^^^^^^^^^

This interface is used to query all DNS Zones and to filter
the output with query parameters.

.. literalinclude:: ../examples/dns/list_zones.py
   :lines: 16-23

Create Zone
^^^^^^^^^^^

This interface is used to create a DNS zone with
parameters.

.. literalinclude:: ../examples/dns/create_zone.py
   :lines: 16-49

Get Zone
^^^^^^^^

This interface is used to get a DNS zone by ID
or an instance of class
:class:`~otcextensions.sdk.dns.v2.zone.Zone`.

.. literalinclude:: ../examples/dns/get_zone.py
   :lines: 16-24

Find Zone
^^^^^^^^^

This interface is used to find a DNS zone by id or name.

.. literalinclude:: ../examples/dns/find_zone.py
   :lines: 16-24

Update Zone
^^^^^^^^^^^

This interface is used to update DNS zone parameters by
id or an instance of class
:class:`~otcextensions.sdk.dns.v2.zone.Zone`.

.. literalinclude:: ../examples/dns/update_zone.py
   :lines: 16-28

Delete Zone
^^^^^^^^^^^

This interface is used to delete a DNS zone by
id or an instance of class
:class:`~otcextensions.sdk.dns.v2.zone.Zone`.

.. literalinclude:: ../examples/dns/delete_zone.py
   :lines: 16-23

Nameserver
----------

List Nameservers
^^^^^^^^^^^^^^^^

This interface is used to query all DNS Nameservers of a zone and to filter
the output with query parameters.

.. literalinclude:: ../examples/dns/list_nameservers.py
   :lines: 16-23

Nameserver
----------

List Nameservers
^^^^^^^^^^^^^^^^

This interface is used to query all DNS Nameservers of a zone and to filter
the output with query parameters.

.. literalinclude:: ../examples/dns/list_nameservers.py
   :lines: 16-23
