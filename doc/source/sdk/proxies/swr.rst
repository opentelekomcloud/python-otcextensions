SWR API
=======

.. automodule:: otcextensions.sdk.swr.v2._proxy

The Software Repository for Containers Service Class
----------------------------------------------------

SoftWare Repository for Container (SWR) high-level interface is
available through the ``swr`` member of a
:class:`~openstack.connection.Connection` object.  The ``swr`` member
will only be added if the ``otcextensions.sdk.register_otc_extensions(conn)``
method is called.

Organization Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.swr.v2._proxy.Proxy
  :noindex:
  :members: create_organization, get_organization, organizations,
            delete_organization, find_organization

Organization Permissions Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.swr.v2._proxy.Proxy
  :noindex:
  :members: create_organization_permissions, organization_permissions,
            delete_organization_permissions, update_organization_permissions

Repository Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.swr.v2._proxy.Proxy
  :noindex:
  :members: create_repository, delete_repository, get_repository,
            repositories, update_repository

Repository Permissions Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.swr.v2._proxy.Proxy
  :noindex:
  :members: create_repository_permissions, repository_permissions,
            delete_repository_permissions, update_repository_permissions

Domain Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.swr.v2._proxy.Proxy
  :noindex:
  :members: create_domain, delete_domain, domains,
            update_domain, get_domain
