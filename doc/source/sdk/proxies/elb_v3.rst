ELB v3 API
================

For details on how to use database, see /sdk/guides/rds (NEEDS TO BE DONE)

.. automodule:: otcextensions.sdk.vlb.v3._proxy

The ELB Class
------------------

The database high-level interface is available through the ``elb`` member of a
:class:`~openstack.connection.Connection` object.  The ``elb`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

LoadBalancer Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: create_load_balancer, get_load_balancer,
            get_load_balancer_statistics, load_balancers,
            delete_load_balancer, find_load_balancer,
            update_load_balancer

Listener Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: listeners

Quota Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: quotas

AvailabilityZone Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: availability_zones

Flavor Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.vlb.v3._proxy.Proxy
  :noindex:
  :members: flavors, get_flavor, find_flavor