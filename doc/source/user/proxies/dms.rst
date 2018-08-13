DMS API
=======

.. automodule:: otcextensions.sdk.dms.v1._proxy

The Distributed Message Service Class
-------------------------------------

The dms high-level interface is available through the ``dms``
member of a :class:`~openstack.connection.Connection` object.  The
``dms`` member will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Queue Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dms.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.queues
   .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.create_queue
   .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.get_queue
   .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.delete_queue


Message Group Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dms.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.groups
  .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.create_group
  .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.delete_group

DMS Quota Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dms.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.dms.v1._proxy.Proxy.quotas
