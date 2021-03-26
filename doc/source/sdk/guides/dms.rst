Distributed Message Service (DMS)
=================================

.. contents:: Table of Contents
   :local:

DMS is a fully-managed, high-performance message queuing service that
supports normal queues, first-in-first-out (FIFO) queues,
Kafka queues, and Kafka premium instances.
It is compatible with HTTP and TCP, and provides a flexible
and reliable asynchronous communication mechanism
for distributed applications.
Normal and FIFO queues feature low-latency and high reliability.
They support dead letter messages for handling exceptions.
In normal queues, partitions ensure higher concurrency.
Kafka queues support high-throughput and high-reliability modes.
A Kafka queue is equivalent to a topic. The storage space and
network bandwidth resources are allocated by the system,
without requiring you to make choices.
Kafka premium instances use physically isolated computing,
storage, and bandwidth resources.
You can customize partitions and replicas for Kafka topics in the instances,
and configure the network bandwidth as required.
The instances can be used right out of the box,
taking off the deployment and O&M pressure for you
so that you can focus on developing your services.

DMS Queues
----------

A message queue is a container that receives and stores message files.
By default, 5 queues can be created under a project.
Different messages in one queue can be retrieved
by multiple consumers at the same time.

List Queues
^^^^^^^^^^^

This interface is used to query all DMS Queues and to filter
the output with query parameters.

.. literalinclude:: ../examples/dms/list_queues.py
   :lines: 16-22

Create Queue
^^^^^^^^^^^^

This interface is used to create a Queue with
parameters.

.. literalinclude:: ../examples/dms/create_queue.py
   :lines: 16-27

Get Queue
^^^^^^^^^

This interface is used to get a Queue by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.queue.Queue`.

.. literalinclude:: ../examples/dms/get_queue.py
   :lines: 16-23

Find Queue
^^^^^^^^^^

This interface is used to find a Queue by ID
or name.

.. literalinclude:: ../examples/dms/find_queue.py
   :lines: 16-23

Delete Queue
^^^^^^^^^^^^

This interface is used to delete a Queue by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.queue.Queue`.

.. literalinclude:: ../examples/dms/delete_queue.py
   :lines: 16-23

DMS Queue Groups
----------------

A consumer group is used to group consumers.
A maximum of three consumer groups can be created in each queue.
Messages in one queue can be retrieved once by each consumer group.
Messages acknowledged by one consumer group are no longer available
to that consumer group but still available to other consumer groups.
Consumers in the same consumer group can retrieve
different messages from one queue at the same time.

List Queue Groups
^^^^^^^^^^^^^^^^^

This interface is used to query all groups of a Queue
and to filter the output with query parameters.

.. literalinclude:: ../examples/dms/list_queue_groups.py
   :lines: 16-23

Create Queue Group
^^^^^^^^^^^^^^^^^^

This interface is used to create a Queue Group with
parameters.

.. literalinclude:: ../examples/dms/create_queue_group.py
   :lines: 16-26

Find Queue Group
^^^^^^^^^^^^^^^^

This interface is used to find a Queue Group by ID
or name.

.. literalinclude:: ../examples/dms/find_queue_group.py
   :lines: 16-25

Delete Queue Group
^^^^^^^^^^^^^^^^^^

This interface is used to delete a Queue Group by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.group.Group`.

.. literalinclude:: ../examples/cce/delete_cluster_node.py
   :lines: 16-25

DMS messages
------------

Messages are JavaScript object notation (JSON) objects
used for transmitting information.
They can be sent one by one or in batches.
Sending messages in batches can be achieved only
through calling DMS application programming interfaces (APIs).

Send message
^^^^^^^^^^^^

This interface is used to send a message with
parameters.

.. literalinclude:: ../examples/dms/send_messages.py
   :lines: 16-42

Consume message
^^^^^^^^^^^^^^^

This interface is used to consume a queue's message by Queue- and Group-ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.queue.Queue`
and
:class:`~otcextensions.sdk.dms.v1.group.Group`.

.. literalinclude:: ../examples/dms/consume_message.py
   :lines: 16-26

Confirm message
^^^^^^^^^^^^^^^

This interface is used to confirm consumed messages by a list of
class
:class:`~otcextensions.sdk.dms.v1.message.Messages`.

.. literalinclude:: ../examples/dms/confirm_message.py
   :lines: 16-38

DMS Instances
-------------

Kafka premium instances use physically isolated computing,
storage, and bandwidth resources.
You can customize partitions and replicas
for Kafka topics in the instances,
and configure the network bandwidth as required.
The instances can be used right out of the box,
taking off the deployment and O&M pressure for you
so that you can focus on developing your services.

List Instances
^^^^^^^^^^^^^^

This interface is used to query all instances
with query parameters

.. literalinclude:: ../examples/dms/list_instances.py
   :lines: 16-22

Find Instance
^^^^^^^^^^^^^

This interface is used to find an Instance by ID
or name

.. literalinclude:: ../examples/dms/find_instance.py
   :lines: 16-23

Get Instance
^^^^^^^^^^^^

This interface is used to get Instance by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.instance.Instance`.

.. literalinclude:: ../examples/cce/get_job.py
   :lines: 16-24

Create Instance
^^^^^^^^^^^^^^^

This interface is used to create an Instance with
parameters.

.. literalinclude:: ../examples/dms/create_instance.py
   :lines: 16-35

Delete Instance
^^^^^^^^^^^^^^^

This interface is used to delete an Instance by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.instance.Instance`.

.. literalinclude:: ../examples/dms/delete_instance.py
   :lines: 16-25

Update Instance
^^^^^^^^^^^^^^^

This interface is used to update an Instance by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.instance.Instance`.

.. literalinclude:: ../examples/dms/create_instance.py
   :lines: 16-28

Restart Instance
^^^^^^^^^^^^^^^^

This interface is used to restart an Instance by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.instance.Instance`.

.. literalinclude:: ../examples/dms/restart_instance.py
   :lines: 16-25

DMS Instance Topics
-------------------

After creating a Kafka premium instance,
you must create a topic in the instance
for creating and retrieving messages.

List Instance Topics
^^^^^^^^^^^^^^^^^^^^

This interface is used to query all instance topics
with query parameters

.. literalinclude:: ../examples/dms/list_instance_topics.py
   :lines: 16-25

Create Instance Topic
^^^^^^^^^^^^^^^^^^^^^

This interface is used to create an Instance topic with
parameters.

.. literalinclude:: ../examples/dms/create_instance_topic.py
   :lines: 16-28

Delete Instance Topic
^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete an Instance topic by ID
or an instance of class
:class:`~otcextensions.sdk.dms.v1.instance.Instance`.

.. literalinclude:: ../examples/dms/delete_instance.py
   :lines: 16-25

Misc
----

Extra APIs allow querying of DMS specific data.

List Instance Availability Zones
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all instance AZ's.

.. literalinclude:: ../examples/dms/list_instance_az_zones.py
   :lines: 16-22

List Products
^^^^^^^^^^^^^

This interface is used to query all supported DMS products.

.. literalinclude:: ../examples/dms/list_instance_products.py
   :lines: 16-22

List Maintenance Windows
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Maintenance Windows.

.. literalinclude:: ../examples/dms/list_maintenance_windows.py
   :lines: 16-22
