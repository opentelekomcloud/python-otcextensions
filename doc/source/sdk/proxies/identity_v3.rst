Identity API v3
===============

.. automodule:: otcextensions.sdk.identity.v3._proxy

The Identity v3 Class
---------------------

The identity high-level interface is available through the ``identity``
member of a :class:`~openstack.connection.Connection` object.  The
``identity`` member will only be added if the service is detected.

Agency Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_agency, update_agency, delete_agency,
            get_agency, find_agency, agencies,
            agency_project_roles, check_agency_project_role,
            grant_agency_project_role, revoke_agency_project_role,
            agency_domain_roles, check_agency_domain_role,
            grant_agency_domain_role, revoke_agency_domain_role,

Credential Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_credential, update_credential, delete_credential,
            get_credential, find_credential, credentials

Domain Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_domain, update_domain, delete_domain, get_domain,
            find_domain, domains

Endpoint Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_endpoint, update_endpoint, delete_endpoint, get_endpoint,
            find_endpoint, endpoints

Group Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_group, update_group, delete_group, get_group, find_group,
            groups

Policy Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_policy, update_policy, delete_policy, get_policy,
            find_policy, policies

Project Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_project, update_project, delete_project, get_project,
            find_project, projects

Region Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_region, update_region, delete_region, get_region,
            find_region, regions

Role Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_role, update_role, delete_role, get_role, find_role, roles

Role Assignment Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: role_assignments, role_assignments_filter,
            assign_project_role_to_user, unassign_project_role_from_user,
            assign_project_role_to_group, unassign_project_role_from_group

Service Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_service, update_service, delete_service, get_service,
            find_service, services

User Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_user, update_user, delete_user, get_user, find_user, users,
            user_projects

Security Token Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.identity.v3._proxy.Proxy
  :noindex:
  :members: create_security_token
