Resources and Attributes
========================

Open Telekom Cloud Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1

   Anti DDoS Service (Anti-DDoS) <anti_ddos/index>
   AutoScaling Service (AS) <auto_scaling/index>
   Cloud Backup and Recovery Service (CBR) <cbr/index>
   Cloud Container Engine (CCE) <cce/index>
   Cloud Eye Service (CES) <ces/index>
   Cloud Search Service (CSS) <css/index>
   Cloud Trace Service (CTS) <cts/index>
   Data Ingestion Service (DIS) <dis/index>
   Data Warehouse Service (DWS) <dws/index>
   Dedicated Host Service (DeH) <deh/index>
   Dedicated Load Balancer (DLB) <vlb/index>
   Direct Connect (DCAAS) <dcaas/index>
   Distributed Cache Service (DCS) <dcs/index>
   Distributed Message Service (DMS) <dms/index>
   Document Database Service (DDS) <dds/index>
   Domain Name Service (DNS) <dns/index>
   FunctionGraph Service (FGS) <function_graph/index>
   Identity Service (IAM) <identity/index>
   Key Management Service (KMS) <kms/index>
   Log Tank Service (LTS) <lts/index>
   MapReduce Service (MRS) <mrs/index>
   ModelArts Service (MA) <modelarts/index>
   Network Address Translation (NAT) <nat/index>
   Object Block Storage (OBS) <obs/index>
   Relational Database Service (RDS) <rds/index>
   Shared File System Turbo (SFS Turbo) <sfsturbo/index>
   Simple Message Notification Service (SMN) <smn/index>
   Storage Disaster Recovery Service (SDRS) <sdrs/index>
   Software Repository for Containers Service (SWR) <swr/index>
   Virtual Private Cloud (VPC) <vpc/index>
   VPC Endpoint (VPCEP) <vpcep/index>
   Web Application Firewall (WAF) <waf/index>
   Tag Management Service (TMS) <tms/index>
   Image Management Service (IMS) <ims/index>
   ApiGateway Service (AGS) <apig/index>

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
