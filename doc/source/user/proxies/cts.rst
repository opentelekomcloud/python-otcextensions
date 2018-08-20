CTS API
=======

.. automodule:: otcextensions.sdk.cts.v1._proxy

The Distributed Message Service Class
-------------------------------------

The CTS high-level interface is available through the ``cts``
member of a :class:`~openstack.connection.Connection` object.  The
``cts`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Trace Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cts.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.cts.v1._proxy.Proxy.traces

Trackers Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cts.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.cts.v1._proxy.Proxy.get_tracker
  .. automethod:: otcextensions.sdk.cts.v1._proxy.Proxy.create_tracker
  .. automethod:: otcextensions.sdk.cts.v1._proxy.Proxy.update_tracker
  .. automethod:: otcextensions.sdk.cts.v1._proxy.Proxy.delete_tracker
