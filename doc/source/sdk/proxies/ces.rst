CES API
=======

.. automodule:: otcextensions.sdk.ces.v1._proxy

The Cloud Eye Service Class
---------------------------

The CES high-level interface is available through the ``ces``
member of a :class:`~openstack.connection.Connection` object.  The
``ces`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Alarm Rule Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ces.v1._proxy.Proxy
  :noindex:
  :members: alarms, get_alarm, create_alarm, delete_alarm, find_alarm,
           switch_alarm_state

Monitoring Data Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ces.v1._proxy.Proxy
  :noindex:
  :members: metric_data

Miscellaneous Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ces.v1._proxy.Proxy
  :noindex:
  :members: metrics, quotas, event_data
