KMS API
=======

.. automodule:: otcextensions.sdk.kms.v1._proxy

The KeyManagementService Class
------------------------------

The kms high-level interface is available through the ``kms``
member of a :class:`~openstack.connection.Connection` object.  The
``kms`` member will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

CMK (Customer Master Key) Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.kms.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.keys
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.create_key
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.get_key
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.find_key
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.enable_key
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.disable_key
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.schedule_key_deletion
   .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.cancel_key_deletion


DEK (Data Encryption Key) Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.kms.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.create_datakey
  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.create_datakey_wo_plain
  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.encrypt_datakey
  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.decrypt_datakey

Other Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.kms.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.generate_random
  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.get_instance_number
  .. automethod:: otcextensions.sdk.kms.v1._proxy.Proxy.quotas
