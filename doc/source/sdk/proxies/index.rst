Service Proxies
===============

.. toctree::
   :maxdepth: 1

   Anti DDoS Service <anti_ddos>
   AutoScaling Service <auto_scaling>
   Cloud Container Engine v1<cce_v1>
   Cloud Container Engine v2<cce_v3>
   Cloud Trace Service <cts>
   Distributed Cache Service <dcs>
   Dedicated Host Service <deh>
   Distributed Message Service <dms>
   DNS Service <dns>
   Key Management Service <kms>
   Object Block Storage <obs>
   Volume Backup Service <volume_backup>
   Relational Database Service RDS V1 <rds_v1>
   Relational Database Service RDS V3 <rds_v3>

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
   Identity v2 <https://docs.openstack.org/openstacksdk/latest/user/proxies/identity_v2>
   Identity v3 <https://docs.openstack.org/openstacksdk/latest/user/proxies/identity_v3>
   Image v1 <https://docs.openstack.org/openstacksdk/latest/user/proxies/image_v1>
   Image v2 <https://docs.openstack.org/openstacksdk/latest/user/proxies/image_v2>
   Key Manager <https://docs.openstack.org/openstacksdk/latest/user/proxies/key_manager>
   Load Balancer <https://docs.openstack.org/openstacksdk/latest/user/proxies/load_balancer_v2>
   Message v2 <https://docs.openstack.org/openstacksdk/latest/user/proxies/message_v2>
   Network <https://docs.openstack.org/openstacksdk/latest/user/proxies/network>
   Object Store <https://docs.openstack.org/openstacksdk/latest/user/proxies/object_store>
   Orchestration <https://docs.openstack.org/openstacksdk/latest/user/proxies/orchestration>
   Workflow <https://docs.openstack.org/openstacksdk/latest/user/proxies/workflow>

