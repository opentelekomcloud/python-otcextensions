Distributed Cache Service (DCS)
===============================

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

A Distributed Cache Service Instance is a Redis instance on top of
Open Telekom Cloud.

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
   :lines: 16-66

Get Instance
^^^^^^^^^^^^

This interface is used to get a DCS instance by ID
or an instance of class
:class:`~otcextensions.sdk.dcs.v1.instance.Instance`.

.. literalinclude:: ../examples/dcs/get_instance.py
   :lines: 16-24

Find Instance
^^^^^^^^^^^^^

This interface is used to find a DCS instance by
name or id.

.. literalinclude:: ../examples/dcs/find_instance.py
   :lines: 16-24

Update Instance
^^^^^^^^^^^^^^^

This interface is used to update a DCS instance by
name or id.

.. literalinclude:: ../examples/dcs/update_instance.py
   :lines: 16-27

Delete Instance
^^^^^^^^^^^^^^^

This interface is used to delete a DCS instance by
id or an instance of class
:class:`~otcextensions.sdk.dcs.v1.instance.Instance`.

.. literalinclude:: ../examples/dcs/delete_instance.py
   :lines: 16-23

Extend Instance
^^^^^^^^^^^^^^^

This interface is used to extend a DCS instance with additional RAM.

.. literalinclude:: ../examples/dcs/extend_instance.py
   :lines: 16-23

Stop Instance
^^^^^^^^^^^^^

This interface is used to stop a DCS instance.

.. literalinclude:: ../examples/dcs/stop_instance.py
   :lines: 16-23

Start Instance
^^^^^^^^^^^^^^

This interface is used to start a DCS instance.

.. literalinclude:: ../examples/dcs/start_instance.py
   :lines: 16-23

Restart Instance
^^^^^^^^^^^^^^^^

This interface is used to restart a DCS instance.

.. literalinclude:: ../examples/dcs/restart_instance.py
   :lines: 16-23

Change Instance Password
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to change the login password of a DCS instance.

.. literalinclude:: ../examples/dcs/change_instance_password.py
   :lines: 16-28

List Statistics of all Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Statistics of all DCS Instances and
to filter the output with query parameters.

.. literalinclude:: ../examples/dcs/list_statistics.py
   :lines: 16-23

List Config Parameters
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Config Parameters of a DCS Instance
and to filter the output with query parameters.

.. literalinclude:: ../examples/dcs/list_instance_params.py
   :lines: 16-25

Update Instance Config Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update config parameters of a DCS instance.

.. literalinclude:: ../examples/dcs/update_instance_params.py
   :lines: 16-47

Backup DCS Instance
-------------------

This API is used to backup a Distributed Cache Service instance.

List Backups
^^^^^^^^^^^^

This interface is used to query all Backups of a DCS Instance and to filter
the output with query parameters.

.. literalinclude:: ../examples/dcs/list_backups.py
   :lines: 16-24

Create Instance Backup
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to backup a DCS Instance.

.. literalinclude:: ../examples/dcs/create_backup.py
   :lines: 16-27

Delete Instance Backup
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to backup a DCS Instance.

.. literalinclude:: ../examples/dcs/delete_backup.py
   :lines: 16-28

Restore DCS Instances
---------------------

This API is used to restore a Distributed Cache Service instance.

List Restore Records
^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Restore Records.

.. literalinclude:: ../examples/dcs/list_restore_records.py
   :lines: 16-24

Restore Instance
^^^^^^^^^^^^^^^^

This interface is used to restore a DCS Instance.

.. literalinclude:: ../examples/dcs/restore_instance.py
   :lines: 16-27

DCS Service Specifications
--------------------------

This API is used to query the product ID (parameter product_id) which
indicates the specifications of the DCS service you created.

List Service Specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all DCS Service Specifications

.. literalinclude:: ../examples/dcs/list_service_specification.py
   :lines: 16-23
