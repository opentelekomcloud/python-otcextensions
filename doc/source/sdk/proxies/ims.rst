IMS API
=======

.. automodule:: otcextensions.sdk.ims.v2._proxy

The Image Management Service Class
----------------------------------

Image Management Service (IMS) high-level interface is
available through the ``ims`` member of a
:class:`~openstack.connection.Connection` object.  The ``ims`` member
will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)``
method is called.

Image Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.ims.v2._proxy.Proxy
  :noindex:
  :members: create_image
