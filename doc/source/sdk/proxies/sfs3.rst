General Purpose File System (SFS3)
==================================

For details on how to use the service, see :doc:`../guides/sfs3`.

.. automodule:: otcextensions.sdk.sfs3.v1._proxy

The SFS3 Class
--------------

The SFS3 high-level interface is available through the ``sfs3`` member of a
:class:`~openstack.connection.Connection` object.  The ``sfs3`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

File System Operations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sfs3.v1._proxy.Proxy
  :noindex:
  :members: file_systems, get_filesystem, create_filesystem, delete_filesystem, create_acl, get_acl, delete_acl, add_tags, delete_tags, get_tags, get_project_tags, filter_resources_by_tags, count_resources_by_tags
