Relational Database Service (RDS)
=================================

.. contents:: Table of Contents
   :local:

The Relational Database Service offers a demand-oriented use of databases in
the Open Telekom Cloud. The RDS includes twelve flavors for implementing
databases for a wide range of requirements. The current versions of mySQL,
PostgreSQL and MS SQL are available as relational database software. The RDS
offers an automatic backup function and point-in-time recovery for the
previous 35 days. Numerous management tools analyze the performance of the
database. Database operation can be optimized on the basis of resource
utilization over time and the evaluation speed.
The RDS supports high availability, even across different availability zones,
and a mirrored standby database can be added to the primary database. Up to
five read replicas can be added to a database cluster. The RDS is also
available directly via an Elastic IP. Databases can be expanded to up 4 GB
during ongoing operation. It is also possible to upgrade a single-instance
database to an active/standby database. Billing is based on the hourly price
of the selected virtual machines (VMs), while additional storage space for
backups and images is billed in accordance with the method used for the
respective storage variant.

Instance
--------

The minimum management unit of RDS is the DB instance. A DB instance is an
isolated database environment in the cloud. A DB instance can contain multiple
user-created databases, and you can access it by using the same tools and
applications that you use with a stand-alone DB instance. You can create
and modify DB instances using the management console or APIs. RDS does not
have limits on the number of running DB instances. Each DB instance has a DB
instance identifier.

RDS supports the following DB engines:

* MySQL
* PostgreSQL
* Microsoft SQL Server

List Instances
^^^^^^^^^^^^^^

This interface is used to query all RDS instances and to filter the output
with query parameters.

.. literalinclude:: ../examples/rds/list_instances.py
   :lines: 16-23

Create Instance
^^^^^^^^^^^^^^^

This interface is used to create a RDS instance with parameters.

.. literalinclude:: ../examples/rds/create_instance.py
   :lines: 16-59

Get Instance
^^^^^^^^^^^^

This interface is used to get a RDS instance by ID or an instance of class
:class:`~otcextensions.sdk.rds.v3.instance.Instance`.

.. literalinclude:: ../examples/rds/get_instance.py
   :lines: 16-24

Find Instance
^^^^^^^^^^^^^

This interface is used to find an RDS instance by name or id.

.. literalinclude:: ../examples/rds/find_instance.py
   :lines: 16-24

Backup
------

When you create a DB instance, an automated backup policy is enabled by
default. After the DB instance is created, you can modify the policy. RDS will
automatically create full backups for DB instances based on your settings.
Manual backups are user-initiated full backups of DB instances. They are
retained until you delete them manually.

List Backups of an RDS Instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all backups of an RDS instance and to filter
the output with query parameters.

.. literalinclude:: ../examples/rds/list_backups.py
   :lines: 16-23

Create Backup
^^^^^^^^^^^^^

This interface is used to create a backup of an RDS instance with parameters.

.. literalinclude:: ../examples/rds/create_backup.py
   :lines: 16-25

Wait for Backup
^^^^^^^^^^^^^^^

This interface is used to wait for a backup of an RDS instance to be completed.

.. literalinclude:: ../examples/rds/wait_for_backup.py
   :lines: 16-27

Find Backup
^^^^^^^^^^^

This interface is used to find an RDS instance backup by name or id.

.. literalinclude:: ../examples/rds/find_instance.py
   :lines: 16-24

List Backup Download Links
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to list download links of RDS backup.

.. literalinclude:: ../examples/rds/list_backup_download_links.py
   :lines: 16-24

Get Instance Backup Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get the backup policy of a RDS instance by ID.

.. literalinclude:: ../examples/rds/get_instance_backup_policy.py
   :lines: 16-24

Set Instance Backup Policy (ToDo)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get the backup policy of a RDS instance by ID.

.. literalinclude:: ../examples/rds/set_instance_backup_policy.py
   :lines: 16-24

Get Instance Restore Time
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get the restore time of a RDS instance by ID.

.. literalinclude:: ../examples/rds/get_instance_restore_time.py
   :lines: 16-24

Restore Instance
^^^^^^^^^^^^^^^^

This interface is used to restore a RDS instance from existing backup.

.. literalinclude:: ../examples/rds/restore_instance.py
   :lines: 16-25

Configurations (Parameter Template)
-----------------------------------

List Configurations
^^^^^^^^^^^^^^^^^^^

This interface is used to query all RDS configurations and to filter
the output with query parameters.

.. literalinclude:: ../examples/rds/list_configurations.py
   :lines: 16-23

Create Configuration
^^^^^^^^^^^^^^^^^^^^

This interface is used to create a RDS configuration template with parameters.

.. literalinclude:: ../examples/rds/create_configuration.py
   :lines: 16-33

Get Configuration
^^^^^^^^^^^^^^^^^

This interface is used to get a RDS configuration template by ID.

.. literalinclude:: ../examples/rds/get_configuration.py
   :lines: 16-24

Find Configuration
^^^^^^^^^^^^^^^^^^

This interface is used to find a RDS configuration template by name or id.

.. literalinclude:: ../examples/rds/find_configuration.py
   :lines: 16-24

Update Configuration
^^^^^^^^^^^^^^^^^^^^

This interface is used to update a DNS configuration by
using name or an instance of class
:class:`~otcextensions.sdk.rds.v1.configuratino.Configuration` and provide new
attributes.

.. literalinclude:: ../examples/rds/update_configuration.py
   :lines: 16-32

Apply Configuration
^^^^^^^^^^^^^^^^^^^

This interface is used to apply a RDS configuration to existing RDS instances.

.. literalinclude:: ../examples/rds/apply_configuration.py
   :lines: 16-29

Datastores
----------

List Datastore Types
^^^^^^^^^^^^^^^^^^^^

This interface is used to query all RDS Datastore Types and to filter
the output with query parameters.

.. literalinclude:: ../examples/rds/list_datastore_types.py
   :lines: 16-23

List Datastores
^^^^^^^^^^^^^^^

This interface is used to query all RDS Datastores of a RDS database and to
filter the output with query parameters.

.. literalinclude:: ../examples/rds/list_datastores.py
   :lines: 16-24

Flavors
-------

List Flavors
^^^^^^^^^^^^

This interface is used to query all flavors of a given RDS datastore and
datastore version.

.. literalinclude:: ../examples/rds/list_flavors.py
   :lines: 16-26
