DMS API
=======

.. automodule:: otcextensions.sdk.dms.v1._proxy

The Distributed Message Service Class
-------------------------------------

The dms high-level interface is available through the ``dms``
member of a :class:`~openstack.connection.Connection` object.  The
``dms`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Queue Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dms.v1._proxy.Proxy
  :noindex:
  :members: queues, create_queue, get_queue, delete_queue

Message Group Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dms.v1._proxy.Proxy
  :noindex:
  :members: groups, create_group, delete_group

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dms.v1._proxy.Proxy
  :noindex:
  :members: instances, find_instance, get_instance,
            create_instance, update_instance, delete_instance,
            delete_batch, restart_instance, delete_failed,
            topics, create_topic, delete_topic,
            availability_zones, products, maintenance_windows
