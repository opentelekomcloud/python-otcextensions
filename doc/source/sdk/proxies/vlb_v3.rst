DLB v3 API
==========

For details on how to use database, see /sdk/guides/vlb (NEEDS TO BE DONE)

.. automodule:: otcextensions.sdk.vlb.v3._proxy

The VLB Class
-------------

The database high-level interface is available through the ``vlb`` member of a
:class:`~openstack.connection.Connection` object.  The ``vlb`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

AvailabilityZone Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: availability_zones,

Certificate Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: create_certificate, delete_certificate, certificates,
            update_certificate, find_certificate, get_certificate,

Flavor Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: flavors, get_flavor, find_flavor

HealthMonitor Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: find_health_monitor, create_health_monitor,
            get_health_monitor, health_monitors,
            delete_health_monitor, update_health_monitor

Listener Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: create_listener, delete_listener, listeners,
            update_listener, find_listener, get_listener

LoadBalancer Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: create_load_balancer, get_load_balancer,
            get_load_balancer_statistics, load_balancers,
            delete_load_balancer, find_load_balancer,
            update_load_balancer

Member Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: create_member, delete_member, find_member,
            get_member, members, update_member

Pool Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: create_pool, get_pool, pools, delete_pool,
            find_pool, update_pool

Quota Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: quotas
