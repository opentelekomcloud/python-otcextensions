Distributed Cache Service
=========================

.. contents:: Table of Contents
   :local:

Redis is a NoSQL database. It can handle various data structures, but should
not be used for complex data structures; relational databases are better
suited for these. While caching the storage in the RAM allows fast data
access, Redis is ideal for all applications in which speed is the main focus.
However, the storage cache not persistent, meaning that the stored data is
deleted if the virtual machine is switched off.
The Distributed Cache Service is ideal for use as a cache server (e.g. in
order to accelerate the loading times of websites), for real-time analyses,
high-speed transactions, and message queuing. Clusters made up of individual
DCS instances can be used for applications with extremely high performance
requirements. Redis is available in the Open Telekom Cloud as the Distributed
Cache Service. Via the console, the database can be defined in three variants:
as a single-node database for temporary data storage, as a master/standby
database for higher availability, and as a cluster for high performance.
The Distributed Cache Service is billed on an hourly basis in accordance with
the chosen RAM size and type (master/standby or single-node database).

Instances
---------

A Distributed Cache Service Instance is a Redis instance on top of Open Telekom Cloud.

List Instances
^^^^^^^^^^^^^^

This interface is used to query all DCS Instances and to filter
the output with query parameters.

.. literalinclude:: ../examples/dcs/list_instances.py
   :lines: 16-23

Create Instance
^^^^^^^^^^^^^^^

This interface is used to create a DCS instance with
parameters.

.. literalinclude:: ../examples/dcs/create_instance.py
   :lines: 16-47

Get Configuration
^^^^^^^^^^^^^^^^^

This interface is used to get an Auto-Scaling Configuration by ID
or an instance of class
:class:`~otcextensions.sdk.auto_scaling.v1.config.Config`.

.. literalinclude:: ../examples/auto_scaling/get_config.py
   :lines: 16-24

Find Configuration
^^^^^^^^^^^^^^^^^^

This interface is used to find an Auto-Scaling Configuration instance by
name or id.

.. literalinclude:: ../examples/auto_scaling/find_config.py
   :lines: 16-24

Delete Configuration
^^^^^^^^^^^^^^^^^^^^

This interface is used to delete an Auto-Scaling Configuration instance by id
or an instance of class
:class:`~otcextensions.sdk.auto_scaling.v1.config.Config`.

.. literalinclude:: ../examples/auto_scaling/delete_config.py
   :lines: 16-23

Batch Delete Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete multiple Auto-Scaling Configuration instances
by id or an instance of
class :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`.

.. literalinclude:: ../examples/auto_scaling/batch_delete_config.py
   :lines: 16-26


Auto-Scaling Group
------------------

An Auto-Scaling (AS) group consists of a collection of instances that apply
to the same scaling scenario. An AS group specifies parameters, such as the
maximum number of instances, expected number of instances, minimum number
of instances, VPC, subnet, and load balancing. Each user can create a maximum
of 25 AS groups by default.

List Groups
^^^^^^^^^^^

This interface is used to query all Auto-Scaling Groups and to filter
the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_groups.py
   :lines: 16-22

Create Group
^^^^^^^^^^^^

This interface is used to create an Auto-Scaling Group with parameters.

.. literalinclude:: ../examples/auto_scaling/create_group.py
   :lines: 16-37

Get Group
^^^^^^^^^

This interface is used to get an Auto-Scaling Group by ID
or an instance of class
:class:`~otcextensions.sdk.auto_scaling.v1.group.Group`.

.. literalinclude:: ../examples/auto_scaling/get_group.py
   :lines: 16-24

Find Group
^^^^^^^^^^

This interface is used to find an Auto-Scaling Group instance by
name or id.

.. literalinclude:: ../examples/auto_scaling/find_group.py
   :lines: 16-24

Delete Group
^^^^^^^^^^^^

This interface is used to delete an Auto-Scaling Group instance by id or
an instance of class :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`.

.. literalinclude:: ../examples/auto_scaling/delete_group.py
   :lines: 16-23

Pause Group
^^^^^^^^^^^

This interface is used to pause an Auto-Scaling Group instance in
passive state by using id or an instance of
class :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`.

.. literalinclude:: ../examples/auto_scaling/pause_group.py
   :lines: 16-25

Resume Group
^^^^^^^^^^^^

This interface is used to resume an Auto-Scaling Group instance in
active state by using id or an instance of
class :class:`~otcextensions.sdk.auto_scaling.v1.group.Group`.

.. literalinclude:: ../examples/auto_scaling/resume_group.py
   :lines: 16-24

Auto-Scaling Policy
-------------------

An Auto-Scaling (AS) policy defines whether to increase or decrease the number
of instances in an AS group. If the number and the expected number of
instances in an AS group are different due to the execution of the AS policy,
AS automatically adjusts the number of instances to the expected. AS supports
the following policy variants:

* alarm-triggered policy
* periodic policy
* scheduled policy

List Policy
^^^^^^^^^^^

This interface is used to query all Auto-Scaling Policies of an AS group
and to filter the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_policies.py
   :lines: 16-25

Create Policy
^^^^^^^^^^^^^

This interface is used to create an Auto-Scaling Policy with parameters.

.. literalinclude:: ../examples/auto_scaling/create_policy.py
   :lines: 16-35


Get Policy
^^^^^^^^^^

This interface is used to get an Auto-Scaling Policy by ID
or an instance of class
:class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`.

.. literalinclude:: ../examples/auto_scaling/get_policy.py
   :lines: 16-24

Find Policy
^^^^^^^^^^^

This interface is used to find an Auto-Scaling Policy instance by
name or id.

.. literalinclude:: ../examples/auto_scaling/find_policy.py
   :lines: 16-24

Delete Policy
^^^^^^^^^^^^^

This interface is used to delete an Auto-Scaling Policy instance by id
or an instance of class
:class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`.

.. literalinclude:: ../examples/auto_scaling/delete_policy.py
   :lines: 16-23

Update Policy
^^^^^^^^^^^^^

This interface is used to update an Auto-Scaling Policy instance by
using policy's id or an instance of class
:class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy` and provide new
attributes.

.. literalinclude:: ../examples/auto_scaling/update_policy.py
   :lines: 16-39

Pause Policy
^^^^^^^^^^^^

This interface is used to pause an Auto-Scaling Policy instance in
passive state by using id or an instance of
class :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`.

.. literalinclude:: ../examples/auto_scaling/pause_policy.py
   :lines: 16-25

Resume Policy
^^^^^^^^^^^^^

This interface is used to resume an Auto-Scaling Policy instance in
active state by using id or an instance of
class :class:`~otcextensions.sdk.auto_scaling.v1.policy.Policy`.

.. literalinclude:: ../examples/auto_scaling/resume_policy.py
   :lines: 16-25

Execute Policy
^^^^^^^^^^^^^^

This interface is used to execute an Auto-Scaling Policy instance and
run the defined actions.

.. literalinclude:: ../examples/auto_scaling/execute_policy.py
   :lines: 16-25

Auto-Scaling Instance
---------------------

An Auto-Scaling (AS) Instance is the executive unit of an Auto-Scaling group.

List Instances
^^^^^^^^^^^^^^

This interface is used to query all Auto-Scaling Instances of an AS group
and to filter the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_instances.py
   :lines: 16-25

Remove Instance
^^^^^^^^^^^^^^^

This interface is used to remove an Auto-Scaling Instances of an AS group.

.. literalinclude:: ../examples/auto_scaling/remove_instance.py
   :lines: 16-26

Batch Action Instance
^^^^^^^^^^^^^^^^^^^^^

This interface is used to run actions on an Auto-Scaling group by adding
or deleting instance.

.. literalinclude:: ../examples/auto_scaling/batch_instance_action.py
   :lines: 16-37

Auto-Scaling Actions and Quotas
-------------------------------

Auto-Scaling quotas and query scaling action logs can be querried.

List Scaling Actions
^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Auto-Scaling scaling action logs
of an AS group and to filter the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_activities.py
   :lines: 16-27

List User or Group Quota for Auto-Scaling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Auto-Scaling quotas of an AS group
or a user and to filter the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_quotas.py
   :lines: 16-27
