CTS API v3
==========

.. automodule:: otcextensions.sdk.ctsv3.v3._proxy

The Cloud Trace Service Class
-----------------------------

The CTS high-level interface is available through the ``cts``
member of a :class:`~openstack.connection.Connection` object.  The
``cts`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Key Event Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ctsv3.v3._proxy.Proxy
  :noindex:
  :members: create_key_event, update_key_event, delete_key_event, key_events

Trace Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ctsv3.v3._proxy.Proxy
  :noindex:
  :members: traces

Tracker Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ctsv3.v3._proxy.Proxy
  :noindex:
  :members: trackers, create_tracker, delete_tracker, update_tracker

Quota Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ctsv3.v3._proxy.Proxy
  :noindex:
  :members: quotas
