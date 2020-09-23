CTS API
=======

.. automodule:: otcextensions.sdk.cts.v1._proxy

The Cloud Trace Service Class
-----------------------------

The CTS high-level interface is available through the ``cts``
member of a :class:`~openstack.connection.Connection` object.  The
``cts`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Trace Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cts.v1._proxy.Proxy
  :noindex:
  :members: traces

Trackers Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.cts.v1._proxy.Proxy
  :noindex:
  :members: get_tracker, create_tracker, update_tracker, delete_tracker
