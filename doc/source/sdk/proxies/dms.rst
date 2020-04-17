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
