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

List Backups
^^^^^^^^^^^^

This interface is used to query CBR backups and to filter
the output with query parameters.

.. literalinclude:: ../examples/cbr/list_backups.py
   :lines: 16-22

Get Backup
^^^^^^^^^^

This interface is used to get a CBR backup by ID or an instance of
class :class:`~otcextensions.sdk.cbr.v3.backup.Backup`.

.. literalinclude:: ../examples/cbr/get_backup.py
   :lines: 16-23

Find Backup
^^^^^^^^^^^

This interface is used to find a CBR backup by name or ID. The return value
is a instance of class
:class:`~otcextensions.sdk.cbr.v3.backup.Backup`.

.. literalinclude:: ../examples/cbr/find_backup.py
   :lines: 16-23

Delete Backup
^^^^^^^^^^^^^

This interface is used to delete a CBR backup instance by id
or an instance of class
:class:`~otcextensions.sdk.cbr.v3.backup.Backup`.

.. literalinclude:: ../examples/cbr/delete_backup.py
   :lines: 16-23

Restore
-------

Restore Data
^^^^^^^^^^^^

This interface is used to restore data from a backup to server instances or
volumes.

.. literalinclude:: ../examples/cbr/restore_data.py
   :lines: 16-36
