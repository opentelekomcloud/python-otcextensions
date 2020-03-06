Getting started with the OTCExtensions SDK
==========================================

Please note that OTCExtensions provides an extension to the OpenStackSDK.
Please refer to it's documentation for the details <https://docs.openstack.org/openstacksdk/latest/>



User Guides
-----------

These guides walk you through how to make use of the libraries we provide
to work with each OpenStack service. If you're looking for a cookbook
approach, this is where you'll want to begin.

.. toctree::
   :maxdepth: 1

   Plain-simple connect to OTC <guides/connect_otc>
   Configuration <config/index>
   Connect to an OpenStack Cloud Using a Config File <https://docs.openstack.org/openstacksdk/latest/user/guides/connect_from_config>
   Using Cloud Abstration Layer <https://docs.openstack.org/openstacksdk/latest/user/usage>
   Logging <guides/logging>
   Microversions <https://docs.openstack.org/openstacksdk/latest/user/microversions>
   Block Storage <https://docs.openstack.org/openstacksdk/latest/user/guides/block_storage>
   Compute <https://docs.openstack.org/openstacksdk/latest/user/guides/compute>
   Identity <https://docs.openstack.org/openstacksdk/latest/user/guides/identity>
   Image <https://docs.openstack.org/openstacksdk/latest/user/guides/image>
   Key Manager <https://docs.openstack.org/openstacksdk/latest/user/guides/key_manager>
   Message <https://docs.openstack.org/openstacksdk/latest/user/guides/message>
   Network <https://docs.openstack.org/openstacksdk/latest/user/guides/network>
   Object Store <https://docs.openstack.org/openstacksdk/latest/user/guides/object_store>
   Orchestration <https://docs.openstack.org/openstacksdk/latest/user/guides/orchestration>
   RDS <guides/rds>
   OBS <guides/obs>
   AutoScaling <guides/auto_scaling>
   Volume Backup <guides/volume_backup>
   Dedicated Host <guides/deh>

API Documentation
-----------------

OpenStackSDK documentation is available under <https://docs.openstack.org/openstacksdk/latest/user/index.html#api-documentation>


Service APIs are exposed through a two-layered approach. The classes
exposed through our `Connection Interface`_ are
the place to start if you're an application developer consuming an OpenStack
cloud. The `Resource Interface`_ is the layer upon which the
`Connection Interface`_ is built, with methods on Service Proxies accepting
and returning :class:`~openstack.resource.Resource` objects.

The Cloud Abstraction layer has a data model.

.. toctree::
   :maxdepth: 1

   model

Connection Interface
~~~~~~~~~~~~~~~~~~~~

A :class:`~openstack.connection.Connection` instance maintains your cloud
config, session and authentication information providing you with a set of
higher-level interfaces to work with OpenStack services.

.. toctree::
   :maxdepth: 1

   connection

Once you have a :class:`~openstack.connection.Connection` instance, services
are accessed through instances of :class:`~openstack.proxy.Proxy` or
subclasses of it that exist as attributes on the
:class:`~openstack.connection.Connection`.

.. autoclass:: openstack.proxy.Proxy
   :members:

Resource Interface
~~~~~~~~~~~~~~~~~~

The *Resource* layer is a lower-level interface to
communicate with OpenStack services. While the classes exposed by the
Service Proxies build a convenience layer on top of
this, :class:`~openstack.resource.Resource` objects can be
used directly. However, the most common usage of this layer is in receiving
an object from a class in the `Connection Interface_`, modifying it, and
sending it back to the Service Proxies layer, such as to update a resource
on the server.

The following services have exposed :class:`~openstack.resource.Resource`
classes.

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
   Anti DDoS Service <resources/anti_ddos/index>
   AutoScaling Service <resources/auto_scaling/index>
   DNS Service <resources/dns/index>
   Cloud Container Engine <resources/cce/index>
   Cloud Trace Service <resources/cts/index>
   Distributed Cache Service <resources/dcs/index>
   Dedicated Host Service <resources/deh/index>
   Distributed Message Service <resources/dms/index>
   Key Management Service <resources/kms/index>
   Object Block Storage <resources/obs/index>
   RDS <resources/rds/index>

Low-Level Classes
~~~~~~~~~~~~~~~~~

The following classes are not commonly used by application developers,
but are used to construct applications to talk to OpenStack APIs. Typically
these parts are managed through the `Connection Interface`_, but their use
can be customized.

.. toctree::
   :maxdepth: 1

   resource
   utils

Presentations
=============

.. toctree::
   :maxdepth: 1

   multi-cloud-demo
