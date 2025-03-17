ApiGateway
==========

.. automodule:: otcextensions.sdk.apig.v2._proxy

Gateway Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: gateways, create_gateway, wait_for_gateway, get_gateway,
            update_gateway, delete_gateway, get_gateway_progress,
            get_constraints, enable_public_access, update_public_access,
            disable_public_access, modify_gateway_spec, bind_eip, unbind_eip,
            enable_ingress, update_ingress, disable_ingress

AZ Operations
^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: azs

Environment Operations
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_environment, update_environment, environments,
            delete_environment

Api Group Operations
^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_api_group, update_api_group, delete_api_group,
            get_api_group, api_groups, verify_api_group_name


Environment Variables Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_environment_variable, update_environment_variable,
            delete_environment_variable, environment_variables,
            get_environment_variable

Throttling Policies Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: throttling_policies, create_throttling_policy,
            delete_throttling_policy, get_throttling_policy,
            update_throttling_policy, bind_throttling_policy,
            unbind_throttling_policy, unbind_throttling_policies,
            bound_throttling_policy_apis, not_bound_throttling_policy_apis,
            bound_throttling_policies

Api Operations
^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: apis, create_api, delete_api, get_api, update_api,
            publish_api, offline_api, check_api, debug_api,
            publish_apis, offline_apis, api_versions,
            switch_version, api_runtime_definitions,
            api_version_details, take_api_version_offline

Credentials Operations
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_app, get_app, update_app, delete_app,
            apps, verify_app, reset_app_secret, get_app_code,
            create_app_code, generate_app_code, app_codes,
            delete_app_code, quotas

Signature Key Operations
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_signature, update_signature, delete_signature,
            signatures, bind_signature, unbind_signature, bound_signatures,
            not_bound_apis, bound_apis

Excluded Request Throttling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_throttling_excluded_policy,
            update_throttling_excluded_policy,
            delete_throttling_excluded_policy, throttling_excluded_policies


Gateway Features Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: configure_gateway_feature, gateway_features,
            supported_gateway_features

Resource Query Operations
^^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: get_api_quantities, get_api_group_quantities,
            get_app_quantities

Domain Name Operations
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: bind_domain_name, unbind_domain_name,
            update_domain_name_bound, create_certificate_for_domain_name,
            unbind_certificate_from_domain_name, enable_debug_domain_name,
            get_bound_certificate

Certificate Operations
^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: delete_certificate
