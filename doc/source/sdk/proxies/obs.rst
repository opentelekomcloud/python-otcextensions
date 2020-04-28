ObjectBlockStorage OBS API
==========================

For details on how to use database, see /user/guides/obs (NEEDS TO BE DONE)

.. automodule:: otcextensions.sdk.obs.v1._proxy

The OBS Class
-------------

The obs high-level interface is available through the ``obs`` member of a
:class:`~openstack.connection.Connection` object.  The ``obs`` member will only
be added if the ``otcextensions.sdk.register_otc_Extensions(conn)`` method is
called.

Container Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.obs.v1._proxy.Proxy
  :noindex:
  :members: containers, get_container, create_container, delete_container

Object Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.obs.v1._proxy.Proxy
  :noindex:
  :members: objects, get_object, create_object, delete_object, download_object
