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

Get Floating IP Policies
^^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query the Anti-DDoS Policy for a specific Floating
IP by using Floating IP id or an instance of class
:class:`~otcextensions.sdk.anti_ddos.v1.floating_ip.FloatingIP`. Anti-DDoS
must be enabled for the specific Floating IP otherwise an error occures.

.. literalinclude:: ../examples/anti_ddos/get_floating_ip_policies.py
   :lines: 18-25

Update Floating IP Policies
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to update Anti-DDoS Policy attributes.

.. literalinclude:: ../examples/anti_ddos/update_floating_ip_policies.py
   :lines: 16-30

Get Floating IP Status
^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query Anti-DDoS status of a Floating IP by using
id.

.. literalinclude:: ../examples/anti_ddos/get_floating_ip_status.py
   :lines: 16-25

List Floating IP Events
^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query all Anti-DDoS events of a Floating IP by using
id.

.. literalinclude:: ../examples/anti_ddos/list_floating_ip_events.py
   :lines: 16-25

List Floating IP Day Statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query all Anti-DDoS events per day of a Floating IP
by using id.

.. literalinclude:: ../examples/anti_ddos/list_floating_ip_stat_day.py
   :lines: 16-25

List Week Statistics of all Floating IPs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query all Anti-DDoS events per week of all Floating
IPs.

.. literalinclude:: ../examples/anti_ddos/list_floating_ip_stat_week.py
   :lines: 16-23

Alarm Configuration
-------------------

Anti-DDoS alerts can be sent in various ways and notifies in case of defense.

List Alarm Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^

This Interface is used to query Anti-DDoS alarm configurations.

.. literalinclude:: ../examples/anti_ddos/list_configs.py
   :lines: 16-23

