KMS API
=======

.. automodule:: otcextensions.sdk.kms.v1._proxy

The KeyManagementService Class
------------------------------

The kms high-level interface is available through the ``kms`` member of a
:class:`~openstack.connection.Connection` object.  The ``kms`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

CMK (Customer Master Key) Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.kms.v1._proxy.Proxy
  :noindex:
  :members: keys, get_key, find_key, create_key, enable_key, disable_key,
            schedule_key_deletion, cancel_key_deletion

DEK (Data Encryption Key) Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.kms.v1._proxy.Proxy
  :noindex:
  :members: create_datakey, create_datakey_wo_plain, encrypt_datakey,
            decrypt_datakey

Other Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.kms.v1._proxy.Proxy
  :noindex:
  :members: generate_random, get_instance_number, quotas
