Known Issues
============

Since providing services and writing client libraries is decoupled,
sometimes issues arise due to errors in the client or the server side,
or due to a service disruption or degration. This page collects
potential issues. They have been found during digging into the API.

General
-------

* Native service version discovery request to
  https://as.eu-de.otc.t-systems.com/autoscaling-api/ caused
  timeout. AS service is temporarily disabled
* Inconsistent naming between services (AS:create_time,
  KMS:creation_date, CCE:createAt)
* Inconsistent error message structure between services (i.e. KMS vs
  RDS). This prohibits code generalization
* No custom service supports proper version discovery. Leads to error
  messages in the OSC tool and execution delays
* LB: while Neutron LBaaS is "strongly" considered as deprecated and
  no bindings are present in Ansible/OSC it will likely not be
  possible/challenge to upstream this support.
* EVS: volume type list --long returns changing results
* Subnet (in some APIs) is most likely net_id
* Without service discovery and multiple versions it is not possible
  to get the proper service version in SDK. It falls back to first
  entry in the VersionFilter
* Tags require different format ("key=value" vs "key*value")

KMS
---

* service version discovery is broken. On
  https://kms.eu-de.otc.t-systems.com/ it returns {"versions":
  [{"status": "CURRENT", "id": "v1.0", "links": [{"href":
  "https://rts.eu-de.otc.t-systems.com/v1/", "rel": "self"}]}]} In the
  keystoneauth1 it results to
  get_endpoint=https://kms.eu-de.otc.t-systems.com/v1 (instead of
  V1.0). Detailed investigation is expensive, therefore aborted
* does not follow REST, everything is POST with different URLs and not
  even json['action']
* is conceptually far away from Barbican
* API Doc: This API allows you to create a plaintext-free DEK, that
  is, the returned result of this API includes `only the plaintext` of
  the DEK.
* purpose of KMS is not precise. Attributes change their names/meaning
  depending on call
* encryption_context is described to be string, in reality dict is
  expected
* max_length is always expected to be exactly max. Make no sense as a
  param
* list CMK filter by key_state not working as documented
* format of the timestamp is unknown
* no way to get response in English

CCE
---

* required header application/type also for GET
* cluster UUID is hidden in a inline metadata structure, making it
  hard to address it without dirty hacks.  Apis are jumping through
  this structure in anti-rest pattern
* attribute naming: metadata.uuid vs metadata.uid
* undocumented properties of the cluster.spec field (i.e. `cidr`)
* far away from Magnum
* Cluster has both VPC and VPC_ID, in GET VPC is name, in POST it
  should be ID
* Subnet is most likely net_id
* In AS sys disk has type "SYS", in CCE - "root"
* Node delete possible only by name, and not id
* service catalog configuration is broken v1 vs v2(v3) with no
  corrupted discovery and new service type

DCS
---

* In OS DCS is part of Trove. The API is same. In the DCS API is
  similar to RDS, but not easy mappable
* Since Redis 3.0.7 (only available in DCS) lots of critical issues
  (incl. security and possible data corruption), online memory defrag,
  less mem usage were fixed

MRS
---

* Inconsistent naming between services ( data_processing-mrs )

OBS
---

* Has storage class on Bucket level, but in AWS and all corresponding
  tools (also s3cmd, s4cmd, Boto) it is on the Object level

DNS (Designate)
---------------

* Nothing supports private zone (ansible, heat, ~terraform,
  SDK/CLI). Very hard to cover that everywhere
* Zone transfer, slave zone are not present. Modern Designateclient is
  not getting clear with response of designate
* API v2 is not implemented

VBS
---

* Uses offset as a pagination, instead of marker (in docs, in reality
  marker is supported)
* Backup creation takes too long. 1Gb empty volume takes >4
  minutes. Functional tests are not reasonable with that.
* Create policy requires frequency to be set
* Shift implemented stuff to osc

CSS
---

* upon creation httpsEnable is str, upon read - bool
* flavors is not OpenStack compatible

HEAT
----

* very old level, blocking many OpenSource projects, including
  i.e. ansible-openshift, RedhatDNS.
* (to be doublechecked) template version check is likely not done,
  since features of later templates with older version header are
  passing validation (in the ranges of supported versions)
* validate return ok, doesn't mean create will pass (validation errors
  i.e. template version doesn't match, condition on a resource level
  was also added on newton)
* not all CLI calls return result
* Not possible to rely on mountpoint of the
  OS::Cinder::VolumeAttachment - it's ignored
* usage of Server with block_device_mapping_v2, devicename="sdX" and >
  1 device fails. Port is not released leaving system in inconsistent
  state (if router interface is deleted can be cleaned only manually)
* OS::Neutron::LBaaS::HealthMonitor does not support type HTTPS, but
  GUI allows it
* update stack with existing template is missing

Shade/Ansible
-------------

* enabling SNAT through Ansible not possible, since upstream expects
  default as true and sends only false if set
  (shade:_build_external_gateway_info)
* only able to pass SYS volume size if boot_from_volume=True
  (default=false)
* on a play retry port in the subnet changes if exists (change IP) and
  corrupts connection
* No support for load balancer
* Ansible (Heat): https://github.com/ansible/ansible/issues/30786 -
  small fix to see the failure message if stack create/update fails
* Private: yes helps to get public_v4 filled, but it hinders create
  request with auto_ip:true
* add router interface

VPC
---

* VPC uses network wrapped subnets. Simple net with multiple subnets
  is not properly visible in OTC (in VPCs list subnet count includes
  all subnets, but in VPC show subnets are missing)

TMS
---

* How to assign tag to resource from API?

BMS
---

* it is not Ironic, but ECS

Network
-------

* Security Group rule "Any" (value=0) is not working as designed. OSC
  uses defaults, use of 0 results in really 0 as a value. Effect is
  unknown yet

DeH
---

* Tag support is not OS compatible

OpenStack SDK
-------------

* LBaaS: pool.healthmonitor_id according to ref api (and in OTC), but
  in the SDK it is health_monitor_ids (list) (reported under
  https://storyboard.openstack.org/#!/story/2001872). Some other
  attributes missing. pool_member operating_status missing
* LBaaS HM: max_retries_down missing (optional and not present in OTC)

DOC
---

* at least on example of ULB LIST allows filtering, but it is not
  documented
