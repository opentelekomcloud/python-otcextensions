LTS API
=======

.. automodule:: otcextensions.sdk.lts.v2._proxy

The Log Tank Service Class
--------------------------

The nat high-level interface is available through the ``lts``
member of a :class:`~openstack.connection.Connection` object.  The
``lts`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

LTS Group Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.lts.v2._proxy.Proxy
  :noindex:
  :members: create_group, update_group, groups,
            delete_group

LTS Stream Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.lts.v2._proxy.Proxy
  :noindex:
  :members: streams, create_stream, delete_stream
