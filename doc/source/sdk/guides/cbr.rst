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

Policy
------

List CBR Policies
^^^^^^^^^^^^^^^^^

This interface is used to query CBR policies and to filter
the output with query parameters.

.. literalinclude:: ../examples/cbr/list_policies.py
   :lines: 16-22

Get CBR Policy
^^^^^^^^^^^^^^

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

Vault
-----

List CBR Vaults
^^^^^^^^^^^^^^^

This interface is used to query CBR vaults and to filter
the output with query parameters.

.. literalinclude:: ../examples/cbr/list_vaults.py
   :lines: 16-22

Get CBR Vault
^^^^^^^^^^^^^

This interface is used to get a CBR vault by ID or an instance of
class :class:`~otcextensions.sdk.cbr.v3.vault.Vault`.

.. literalinclude:: ../examples/cbr/get_vault.py
   :lines: 16-23

Create CBR Vault
^^^^^^^^^^^^^^^^

This interface is used to create a CBR vault instance with
parameters.

.. literalinclude:: ../examples/cbr/create_vault.py
   :lines: 16-46

Update CBR Vault
^^^^^^^^^^^^^^^^

This interface is used to update a CBR vault instance with
parameters.

.. literalinclude:: ../examples/cbr/update_vault.py
   :lines: 16-29

Delete CBR Vault
^^^^^^^^^^^^^^^^

This interface is used to delete a CBR vault instance by id
or an instance of class
:class:`~otcextensions.sdk.cbr.v3.vault.Vault`.

.. literalinclude:: ../examples/cbr/delete_vault.py
   :lines: 16-23

Bind Policy to CBR Vault
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to bind a CBR policy to a CBR vault.

.. literalinclude:: ../examples/cbr/bind_policy.py
   :lines: 16-26

Unbind Policy to CBR Vault
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to release a CBR policy from a CBR vault.

.. literalinclude:: ../examples/cbr/unbind_policy.py
   :lines: 16-26

Associate resources to CBR Vault
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to add resources to a CBR vault.

.. literalinclude:: ../examples/cbr/associate_resources.py
   :lines: 16-28

Dissociate resources from CBR Vault
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to remove resources from CBR vault.

.. literalinclude:: ../examples/cbr/dissociate_resources.py
   :lines: 16-27

Member
------
This API is used to add a member with whom the backup can be shared. Only
cloud server backups can be shared among tenants in the same region.

List CBR Share Member
^^^^^^^^^^^^^^^^^^^^^

This interface is used to query CBR share members of an existing CBR Backup
and to filter the output with query parameters.

.. literalinclude:: ../examples/cbr/list_members.py
   :lines: 16-25

Get CBR Share Member
^^^^^^^^^^^^^^^^^^^^

This interface is used to get a CBR share member by ID or an instance of
class :class:`~otcextensions.sdk.cbr.v3.member.Member`.

.. literalinclude:: ../examples/cbr/get_member.py
   :lines: 16-25

Add CBR Share Member
^^^^^^^^^^^^^^^^^^^^

This interface is used to add a list of destination project IDs as share
member to a given CBR backup in a source project.

.. literalinclude:: ../examples/cbr/add_member.py
   :lines: 16-24

Update CBR Share Member
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a CBR share member instance with
parameters.

.. literalinclude:: ../examples/cbr/update_member.py
   :lines: 16-28

Delete CBR Share Member
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a CBR share member instance by id
or an instance of class
:class:`~otcextensions.sdk.cbr.v3.member.Member`.

.. literalinclude:: ../examples/cbr/delete_member.py
   :lines: 16-25
