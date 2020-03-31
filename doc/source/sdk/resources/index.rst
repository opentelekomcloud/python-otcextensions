Resources and Attributes
========================

Open Telekom Cloud Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Anti DDoS Service (Anti-DDoS) <anti_ddos/index>
   AutoScaling Service (AS) <auto_scaling/index>
   Cloud Container Engine (CCE) <cce/index>
   Cloud Trace Service (CTS) <cts/index>
   Distributed Cache Service (DCS) <dcs/index>
   Dedicated Host Service (DeH) <deh/index>
   Distributed Message Service (DMS) <dms/index>
   Domain Name Service (DNS) <dns/index>
   Key Management Service (KMS) <kms/index>
   Object Block Storage (OBS) <obs/index>
   Relational Database Service (RDS) <rds/index>

Every resource which is used within the proxy methods have own attributes.
Those attributes define the behavior of the resource which can be a cluster
or a node or anything different logical unit in an OpenStack Cloud. The
*Resource* layer is a lower-level interface to communicate with OpenStack
services. While the classes exposed by the :ref:`service-proxies` build a
convenience layer on top of this, :class:`~openstack.resource.Resource`
objects can be used directly. However, the most common usage of this layer is
in receiving an object from a class in the `Connection Interface_`,
modifying it, and sending it back to the :ref:`service-proxies` layer,
such as to update a resource on the server.

The following services have exposed :class:`~openstack.resource.Resource`
classes.

OpenStack native Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Baremetal <https://docs.openstack.org/openstacksdk/latest/user/resources/baremetal/index>
   Block Storage <https://docs.openstack.org/openstacksdk/latest/user/resources/block_storage/index>
   Clustering <https://docs.openstack.org/openstacksdk/latest/user/resources/clustering/index>
   Compute <https://docs.openstack.org/openstacksdk/latest/user/resources/compute/index>
   Database <https://docs.openstack.org/openstacksdk/latest/user/resources/database/index>
   Identity <https://docs.openstack.org/openstacksdk/latest/user/resources/identity/index>
   Image <https://docs.openstack.org/openstacksdk/latest/user/resources/image/index>
   Key Management <https://docs.openstack.org/openstacksdk/latest/user/resources/key_manager/index>
   Load Balancer <https://docs.openstack.org/openstacksdk/latest/user/resources/load_balancer/index>
   Network <https://docs.openstack.org/openstacksdk/latest/user/resources/network/index>
   Orchestration <https://docs.openstack.org/openstacksdk/latest/user/resources/orchestration/index>
   Object Store <https://docs.openstack.org/openstacksdk/latest/user/resources/object_store/index>
   Workflow <https://docs.openstack.org/openstacksdk/latest/user/resources/workflow/index>
