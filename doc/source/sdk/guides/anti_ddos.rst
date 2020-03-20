Anti-DDoS (AS)
==============

.. contents:: Table of Contents
   :local:

Floating-IP Operations
----------------------

Floating IP operations lists all methods which are used to query and modify
Floating IPs settings related to Anti-DDoS.

List Anti-DDoS Floating IPs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Floating IPs protected by Anti-DDoS and
limit the output with parameters.

.. literalinclude:: ../examples/anti_ddos/list_floating_ips.py
   :lines: 16-23

Protect an Floating IP (not working)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to enable Anti-DDoS on a Floating IP by using IP id or
an instance of class
:class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`.

.. literalinclude:: ../examples/anti_ddos/protect_floating_ip.py
   :lines: 17-23

Unprotect an Floating IP (not working)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to disable Anti-DDoS on a Floating IP by using IP id or
an instance of class
:class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`.

.. literalinclude:: ../examples/anti_ddos/unprotect_floating_ip.py
   :lines: 17-23

Get Policies of a Floating IP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query the Anti-DDoS Policy for a specific Floating
IP by using Floating IP id or an instance of class
:class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`. Anti-DDoS
must be enabled for this IP otherwise an error occures.

.. literalinclude:: ../examples/anti_ddos/get_floating_ip_policies.py
   :lines: 18-25

