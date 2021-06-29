Service Proxies
===============

.. toctree::
   :maxdepth: 1

   Anti DDoS Service (Anti-DDoS) <anti_ddos>
   AutoScaling Service (AS) <auto_scaling>
   Cloud Backup and Recovery Service (CBR) <cbr>
   Cloud Container Engine v1 (CCEv1) <cce_v1>
   Cloud Container Engine v2 (CCE) <cce_v3>
   Cloud Eye Service (CES) <ces>
   Cloud Trace Service (CTS) <cts>
   Distributed Cache Service (DCS) <dcs>
   Document Database Service (DDS) <dds_v3>
   Dedicated Host Service (DeH) <deh>
   Distributed Message Service (DMS) <dms>
   Domain Name Server Service (DNS) <dns>
   Identity Service (IAM) <identity_v3>
   Key Management Service (KMS) <kms>
   Network Address Translation (NAT) <nat>
   Object Block Storage (OBS) <obs>
   Relational Database Service RDS V1 (RDSv1) <rds_v1>
   Relational Database Service RDS V3 (RDS) <rds_v3>
   Simple Message Notification Service (SMN) <smn>
   Volume Backup Service (VBS) <volume_backup>
   Virtual Private Cloud (VPC) <vpc>
   Web Application Firewall (WAF) <waf>

.. _service-proxies:

Service Proxies
---------------

The following service proxies exist on the
:class:`~openstack.connection.Connection`. The service proxies are all always
present on the :class:`~openstack.connection.Connection` object, but the
combination of your ``CloudRegion`` and the catalog of the cloud in question
control which services can be used.

Links to Native OpenStack Service Proxies
-----------------------------------------

.. toctree::
   :maxdepth: 1

   Block Storage <https://docs.openstack.org/openstacksdk/latest/user/proxies/block_storage>
   Compute <https://docs.openstack.org/openstacksdk/latest/user/proxies/compute>
   Database <https://docs.openstack.org/openstacksdk/latest/user/proxies/database>
   Identity v3 <https://docs.openstack.org/openstacksdk/latest/user/proxies/identity_v3>
   Image v2 <https://docs.openstack.org/openstacksdk/latest/user/proxies/image_v2>
   Network <https://docs.openstack.org/openstacksdk/latest/user/proxies/network>
   Object Store <https://docs.openstack.org/openstacksdk/latest/user/proxies/object_store>
   Orchestration <https://docs.openstack.org/openstacksdk/latest/user/proxies/orchestration>
