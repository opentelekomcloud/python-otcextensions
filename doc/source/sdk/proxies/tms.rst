TMS API
=======

.. automodule:: otcextensions.sdk.tms.v1._proxy

The Tag Management Service Class
--------------------------------

Tag Management Service (TMS) high-level interface is
available through the ``tms`` member of a
:class:`~openstack.connection.Connection` object.  The ``tms`` member
will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)``
method is called.

Predefined Tag Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.tms.v1._proxy.Proxy
  :noindex:
  :members: predefined_tags, create_predefined_tag, delete_predefined_tag,
            update_predefined_tag

Resource Tag Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.tms.v1._proxy.Proxy
  :noindex:
  :members: resource_tags, create_resource_tag, delete_resource_tag
