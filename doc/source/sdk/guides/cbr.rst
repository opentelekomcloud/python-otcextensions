Cloud Backup and Recovery (CBR)
===============================

Cloud Backup and Recovery (CBR) enables you to back up Elastic Cloud Servers
(ECSs) and Elastic Volume Service (EVS) disks with ease. If there is a
virus intrusion, accidental deletion, or software or hardware fault, you
can restore data to any point in the past when the data was backed up.
CBR protects your services by ensuring the security and consistency of your
data.

.. contents:: Table of Contents
   :local:

Backup
------

A backup is a copy of the original data that is backed up. A backup is used
to restore the original data.

List CBR Backups
^^^^^^^^^^^^^^^^

This interface is used to query CBR backups and to filter
the output with query parameters.

.. literalinclude:: ../examples/cbr/list_backups.py
   :lines: 16-22

Get CBR Backup
^^^^^^^^^^^^^^

This interface is used to get a CBR backup by ID or an instance of
class :class:`~otcextensions.sdk.cbr.v3.backup.Backup`.

.. literalinclude:: ../examples/cbr/get_backup.py
   :lines: 16-23

Find CBR Backup
^^^^^^^^^^^^^^^

This interface is used to find a CBR backup by name or ID. The return value
is a instance of class
:class:`~otcextensions.sdk.cbr.v3.backup.Backup`.

.. literalinclude:: ../examples/cbr/find_backup.py
   :lines: 16-23

Delete CBR Backup
^^^^^^^^^^^^^^^^^

This interface is used to delete a CBR backup instance by id
or an instance of class
:class:`~otcextensions.sdk.cbr.v3.backup.Backup`.

.. literalinclude:: ../examples/cbr/delete_backup.py
   :lines: 16-23

Backup
------

List CBR Policies
^^^^^^^^^^^^^^^^^

This interface is used to query CBR policies and to filter
the output with query parameters.

.. literalinclude:: ../examples/cbr/list_policies.py
   :lines: 16-22

Get CBR Policies
^^^^^^^^^^^^^^^^

This interface is used to get a CBR policy by ID or an instance of
class :class:`~otcextensions.sdk.cbr.v3.policy.Policy`.

.. literalinclude:: ../examples/cbr/get_policy.py
   :lines: 16-24

Create CBR Policy
^^^^^^^^^^^^^^^^^

This interface is used to create a CBR policy instance with
parameters.

.. literalinclude:: ../examples/cbr/create_policy.py
   :lines: 16-44

Update CBR Policy
^^^^^^^^^^^^^^^^^

This interface is used to update a CBR policy instance with
parameters.

.. literalinclude:: ../examples/cbr/update_policy.py
   :lines: 16-45

Delete CBR Policy
^^^^^^^^^^^^^^^^^

This interface is used to delete a CBR policy instance by id
or an instance of class
:class:`~otcextensions.sdk.cbr.v3.policy.Policy`.

.. literalinclude:: ../examples/cbr/delete_policy.py
   :lines: 16-24

Restore Point (Checkpoint)
--------------------------

Restore points are used to create backups of resources attached to a vault.

Get CBR Restore Point (Checkpoint)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get a CBR restore point by ID or an instance of
class :class:`~otcextensions.sdk.cbr.v3.checkpoint.Checkpoint`.

.. literalinclude:: ../examples/cbr/get_checkpoint.py
   :lines: 16-22

Create CBR Restore Point (Checkpoint)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a CBR Restore point instance with
parameters.

.. literalinclude:: ../examples/cbr/create_checkpoint.py
   :lines: 16-34

Restore
-------

Restore Data
^^^^^^^^^^^^

This interface is used to restore data from a backup to server instances or
volumes.

.. literalinclude:: ../examples/cbr/restore_data.py
   :lines: 16-36
