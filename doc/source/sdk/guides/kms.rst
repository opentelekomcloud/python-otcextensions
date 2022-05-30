Key Management Service (KMS)
============================

.. contents:: Table of Contents
   :local:

The Key Management Service (KMS) of the Open Telekom Cloud generates and
stores public keys for accessing data in the Open Telekom Cloud and
makes them available to the respective user. It combines the essential
security requirements placed on a cloud with high usability, as users can
manage their keys directly via the console.
The KMS ensures secure access to data and is integrated with other Open
Telekom Cloud services. Cloud Trace monitors access to keys and thereby
helps fulfill audit and compliance requirements. During implementation,
the KMS also uses hardware security modules (HSM) for professional
management of key security.
The KMS does not store the data encryption keys (DEK) directly; instead
users receive their DEKs via customer master keys. The hardware security
modules serve to handle encryption and decryption processes, while a
dedicated API is used to access the service. The Open Telekom Cloud also
allows users to deploy their own keys (“bring your own key”). Another
available function is “grant master key,” which allows owners of tenants to
issue temporary permissions for access to encrypted data.

Customer Master Key
-------------------

A Customer Master Key (CMK) is a Key Encryption Key (KEK) created by a user
using KMS. It is used to encrypt and protect Data Encryption Keys (DEKs). One
CMK can be used to encrypt one or multiple DEKs.

You can perform the following operations on
CMKs:

* Creating, querying, enabling, disabling, scheduling the deletion of, and
  canceling the deletion of CMKs
* Importing CMKs and deleting CMK material
* Modifying the aliases and description of CMKs
* Creating, querying, and revoking a grant
* Adding, searching for, editing, and deleting tags
* Enabling key rotation


List Keys
^^^^^^^^^

This interface is used to query all KMS Keys and to filter
the output with query parameters.

.. literalinclude:: ../examples/kms/list_keys.py
   :lines: 16-23

Create Key
^^^^^^^^^^

This interface is used to create a KMS key with
parameters.

.. literalinclude:: ../examples/kms/create_key.py
   :lines: 16-27

Get Key
^^^^^^^

This interface is used to get a KMS key by ID
or an instance of class
:class:`~otcextensions.sdk.kms.v1.key.Key`.

.. literalinclude:: ../examples/kms/get_key.py
   :lines: 16-24

Find Key
^^^^^^^^^

This interface is used to find a KMS key by id or name.

.. literalinclude:: ../examples/kms/find_key.py
   :lines: 16-24

Enable Key
^^^^^^^^^^

This interface is used to enable a KMS key by id or an instance of class
:class:`~otcextensions.sdk.kms.v1.key.Key`.

.. literalinclude:: ../examples/kms/enable_key.py
   :lines: 16-24

Disable Key
^^^^^^^^^^^

This interface is used to disable a KMS key by id or an instance of class
:class:`~otcextensions.sdk.kms.v1.key.Key`.

.. literalinclude:: ../examples/kms/disable_key.py
   :lines: 16-24

Schedule Key Deletion
^^^^^^^^^^^^^^^^^^^^^

This interface is used to schedule the KMS key deletion with a specific
retention time by id or an instance of class
:class:`~otcextensions.sdk.kms.v1.key.Key`.

.. literalinclude:: ../examples/kms/schedule_key_deletion.py
   :lines: 16-23

Cancel Key Deletion
^^^^^^^^^^^^^^^^^^^

This interface is used to cancel the KMS key deletion by key id or an
instance of class
:class:`~otcextensions.sdk.kms.v1.key.Key`.

.. literalinclude:: ../examples/kms/cancel_key_deletion.py
   :lines: 16-23

Data Encryption Key
-------------------

Data Encryption Keys (DEKs) are used to encrypt data.

Create Datakey
^^^^^^^^^^^^^^

This interface is used to create a KMS Datakey with
parameters.

.. literalinclude:: ../examples/kms/create_datakey.py
   :lines: 16-26

Create Datakey without plain Text
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a KMS data encryption key without plain text.

.. literalinclude:: ../examples/kms/create_datakey.py
   :lines: 16-26

Encrypt Datakey
^^^^^^^^^^^^^^^

This interface is used to encrypt a KMS data encryption key.

.. literalinclude:: ../examples/kms/encrypt_datakey.py
   :lines: 16-25

Decrypt Datakey
^^^^^^^^^^^^^^^

This interface is used to decrypt a KMS data encryption key.

.. literalinclude:: ../examples/kms/decrypt_datakey.py
   :lines: 16-27

Miscellaneous
-------------

Generate Random Data
^^^^^^^^^^^^^^^^^^^^

This interface is used to generate random Data.

.. literalinclude:: ../examples/kms/generate_random_data.py
   :lines: 16-23

Get Instance Number
^^^^^^^^^^^^^^^^^^^

This interface is used to get the total number of encrypt key instances.

.. literalinclude:: ../examples/kms/get_instance_number.py
   :lines: 16-23

List KMS quotas
^^^^^^^^^^^^^^^

This interface is used to query all KMS quotas.

.. literalinclude:: ../examples/kms/list_quotas.py
   :lines: 16-23
