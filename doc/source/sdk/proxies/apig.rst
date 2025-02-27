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

Signature Key Operations
^^^^^^^^^^^^^^^^^^^^^^^^
.. autoclass:: otcextensions.sdk.apig.v2._proxy.Proxy
  :noindex:
  :members: create_signature, update_signature, delete_signature,
            signatures, bind_signature, unbind_signature, bound_signatures,
            not_bound_apis, bound_apis
