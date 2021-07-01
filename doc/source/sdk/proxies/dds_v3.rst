Document Database (DDS) API
===========================

For details on how to use dds, see /sdk/guides/dds (NEEDS TO BE DONE)

.. automodule:: otcextensions.sdk.dds.v3._proxy

The DDS Class
-------------

The dds high-level interface is available through the ``dds`` member of a
:class:`~openstack.connection.Connection` object.  The ``dds`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Datastore Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: datastores, datastore_types

Flavor Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: flavors

Instance Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: instances
