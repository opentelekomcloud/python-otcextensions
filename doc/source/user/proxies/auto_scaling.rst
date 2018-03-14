AutoScaling API
===============

For details on how to use database, see :doc:`/user/guides/auto_scaling`

.. automodule:: otcextensions.sdk.auto_scaling.v1._proxy

The AutoScaling Class
---------------------

The AS high-level interface is available through the ``auto_scaling``
member of a :class:`~openstack.connection.Connection` object.  The
``auto_scaling`` member will only be added if the ``otcextensions.sdk.register_otc_Extensions(conn)`` method is called.

Group Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.groups
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.get_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.find_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.create_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.delete_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.resume_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.pause_group
