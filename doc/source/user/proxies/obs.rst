ObjectBlockStorage OBS API
==========================

For details on how to use database, see :doc:`/user/guides/obs`

.. automodule:: otcextensions.sdk.obs.v1._proxy

The OBS Class
-------------

The obs high-level interface is available through the ``obs``
member of a :class:`~openstack.connection.Connection` object.  The
``obs`` member will only be added if the ``otcextensions.sdk.register_otc_Extensions(conn)`` method is called.

Container Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.obs.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.containers
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.get_container
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.create_container
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.delete_container

Object Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.obs.v1._proxy.Proxy

   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.objects
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.get_object
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.create_object
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.delete_object
   .. automethod:: otcextensions.sdk.obs.v1._proxy.Proxy.download_object
