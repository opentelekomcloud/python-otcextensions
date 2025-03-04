ApiGateway Service (AGS)
========================

.. contents:: Table of Contents
   :local:

API Gateway (APIG) is a high-performance, high-availability,
and high-security API hosting service that helps you build,
manage, and deploy APIs at any scale. With just a few clicks,
you can integrate internal systems, and selectively expose
capabilities with minimal costs and risks.

Gateway
_______

A Gateway is a service that acts as an intermediary between
clients and backend services, providing a centralized point
of control for processing API requests. It enables management
of access, security, routing, scalability, and monitoring of
APIs.


Create Gateway
^^^^^^^^^^^^^^

This example demonstrates how to create a new gateway.

.. literalinclude:: ../examples/apig/create_gateway.py
   :lines: 16-31

Delete Gateway
^^^^^^^^^^^^^^

This example demonstrates how to delete an existing gateway.

.. literalinclude:: ../examples/apig/delete_gateway.py
   :lines: 16-21

List Gateways
^^^^^^^^^^^^^

This example demonstrates how to list all gateways.

.. literalinclude:: ../examples/apig/list_gateways.py
   :lines: 16-25

Get Gateway Details
^^^^^^^^^^^^^^^^^^^

This example demonstrates how to retrieve details of a specific gateway.

.. literalinclude:: ../examples/apig/get_gateway.py
   :lines: 16-21

Update Gateway
^^^^^^^^^^^^^^

This example demonstrates how to update an existing gateway.

.. literalinclude:: ../examples/apig/update_gateway.py
   :lines: 16-25

Bind EIP
^^^^^^^^

This example demonstrates how to bind an Elastic IP (EIP) to a gateway.

.. literalinclude:: ../examples/apig/bind_eip.py
   :lines: 16-24

Unbind EIP
^^^^^^^^^^

This example demonstrates how to unbind an Elastic IP (EIP) from a gateway.

.. literalinclude:: ../examples/apig/unbind_eip.py
   :lines: 16-21


Update Public Inbound Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to update public inbound access for a gateway.

.. literalinclude:: ../examples/apig/update_ingress.py
   :lines: 16-26

Enable Public Inbound Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to enable public inbound access for a gateway.

.. literalinclude:: ../examples/apig/enable_ingress.py
   :lines: 16-25

Disable Public Inbound Access
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to disable public inbound access for a gateway.

.. literalinclude:: ../examples/apig/disable_ingress.py
   :lines: 16-21

Enable Public Access
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to enable public access for a gateway.

.. literalinclude:: ../examples/apig/enable_public_access.py
   :lines: 16-25

Update Public Access
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to update public access settings for a gateway.

.. literalinclude:: ../examples/apig/update_public_access.py
   :lines: 16-26

Disable Public Access
^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to disable public access for a gateway.

.. literalinclude:: ../examples/apig/disable_public_access.py
   :lines: 16-21

Get Gateway Constraints
^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to retrieve the constraints and
limitations of a gateway.

.. literalinclude:: ../examples/apig/get_constraints.py
   :lines: 16-21

Get Gateway Creation Progress
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to check the progress of a gateway
creation process.

.. literalinclude:: ../examples/apig/get_gateway_progress.py
   :lines: 16-21

Modify Gateway Specifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to modify the specifications of an
existing gateway.

.. literalinclude:: ../examples/apig/modify_gateway_spec.py
   :lines: 16-25

AZs
___

List Azs
^^^^^^^^

This example demonstrates how to list the availability zones (AZs)
supported by API Gateway.

.. literalinclude:: ../examples/apig/list_azs.py
   :lines: 16-25

Environment
___________

Create Environment
^^^^^^^^^^^^^^^^^^

This example demonstrates how to create a new environment within
a specific API Gateway.

.. literalinclude:: ../examples/apig/create_env.py
   :lines: 16-25


Update Environment
^^^^^^^^^^^^^^^^^^

This example demonstrates how to update an existing environment
within a specific API Gateway.

.. literalinclude:: ../examples/apig/update_env.py
   :lines: 16-26


Delete Environment
^^^^^^^^^^^^^^^^^^

This example demonstrates how to delete an existing environment
from a specific API Gateway.

.. literalinclude:: ../examples/apig/delete_env.py
   :lines: 16-21


List Environments
^^^^^^^^^^^^^^^^^

This example demonstrates how to list all environments associated
with a specific API Gateway.

.. literalinclude:: ../examples/apig/list_envs.py
   :lines: 16-20

Api Group
_________

Create Api Group
^^^^^^^^^^^^^^^^

This example demonstrates how to create a new API group in the API Gateway.

.. literalinclude:: ../examples/apig/create_api_group.py
   :lines: 16-25

Update Api Group
^^^^^^^^^^^^^^^^

This example demonstrates how to update an existing API group
in the API Gateway.

.. literalinclude:: ../examples/apig/update_api_group.py
   :lines: 16-27

Delete Api Group
^^^^^^^^^^^^^^^^

This example demonstrates how to delete an existing API group from
the API Gateway.

.. literalinclude:: ../examples/apig/delete_api_group.py
   :lines: 16-21

List Api Groups
^^^^^^^^^^^^^^^

This example demonstrates how to list all API groups associated
with a specific API Gateway.

.. literalinclude:: ../examples/apig/list_api_groups.py
   :lines: 16-20

Get Api Group
^^^^^^^^^^^^^

This example demonstrates how to retrieve details of a specific
API group from the API Gateway.

.. literalinclude:: ../examples/apig/get_api_group.py
   :lines: 16-21

Verify Api Group Name
^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to verify whether a given API group
name is available in the API Gateway.

.. literalinclude:: ../examples/apig/verify_api_group_name.py
   :lines: 16-23

Creating a Variable
^^^^^^^^^^^^^^^^^^^

This example demonstrates how to define environment variables.

.. literalinclude:: ../examples/apig/create_env_variable.py
   :lines: 16-30

Deleting a Variable
^^^^^^^^^^^^^^^^^^^

This example demonstrates how to delete environment variable.

.. literalinclude:: ../examples/apig/delete_env_variable.py
   :lines: 16-23

Querying Variable Details
^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the details of an environment variable.

.. literalinclude:: ../examples/apig/get_env_variable.py
   :lines: 16-24

Querying Environment Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query all environment
variables under an API group.

.. literalinclude:: ../examples/apig/list_env_variables.py
   :lines: 16-23

Modifying a Variable
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to modify an environment variable.

.. literalinclude:: ../examples/apig/update_env_variable.py
   :lines: 16-27

Creating a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to create throttling policy.

.. literalinclude:: ../examples/apig/create_throttling_policy.py
   :lines: 16-38

Modifying a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to update throttling policy.

.. literalinclude:: ../examples/apig/update_throttling_policy.py
   :lines: 16-34

Deleting a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to delete throttling policy.

.. literalinclude:: ../examples/apig/delete_throttling_policy.py
   :lines: 16-23

Querying Request Throttling Policies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query all throttling policies.

.. literalinclude:: ../examples/apig/list_throttling_policies.py
   :lines: 16-21

Querying Details of a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to get throttling policy.

.. literalinclude:: ../examples/apig/get_throttling_policy.py
   :lines: 16-24

Creating an API
^^^^^^^^^^^^^^^

This example demonstrates how to create an API.

.. literalinclude:: ../examples/apig/create_api.py
   :lines: 16-45

Modifying an API
^^^^^^^^^^^^^^^^

This example demonstrates how to update an API.

.. literalinclude:: ../examples/apig/update_api.py
   :lines: 16-46

Deleting an API
^^^^^^^^^^^^^^^

This example demonstrates how to delete an API.

.. literalinclude:: ../examples/apig/delete_api.py
   :lines: 16-23

Querying API Details
^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to get an API.

.. literalinclude:: ../examples/apig/get_api.py
   :lines: 16-24

Querying APIs
^^^^^^^^^^^^^

This example demonstrates how to list an APIs.

.. literalinclude:: ../examples/apig/list_apis.py
   :lines: 16-20

Publishing an API
^^^^^^^^^^^^^^^^^

This example demonstrates how to publish an API.

.. literalinclude:: ../examples/apig/publish_api.py
   :lines: 16-25

Take API offline
^^^^^^^^^^^^^^^^

This example demonstrates how to take API offline.

.. literalinclude:: ../examples/apig/offline_api.py
   :lines: 16-25

Verifying the API Definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to verify the API definition.

.. literalinclude:: ../examples/apig/check_api.py
   :lines: 16-27

Debugging an API
^^^^^^^^^^^^^^^^

This example demonstrates how to debug an API in a specified environment.

.. literalinclude:: ../examples/apig/debug_api.py
   :lines: 16-30

Publishing APIs
^^^^^^^^^^^^^^^

This example demonstrates how to publish multiple APIs in an environment.

.. literalinclude:: ../examples/apig/publish_apis.py
   :lines: 16-25

Taking APIs Offline
^^^^^^^^^^^^^^^^^^^

This example demonstrates how to remove multiple APIs from the environment.

.. literalinclude:: ../examples/apig/offline_apis.py
   :lines: 16-25

Querying Historical Versions of an API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the historical versions of an API.

.. literalinclude:: ../examples/apig/list_api_versions.py
   :lines: 16-23

Switching the Version of an API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to switch the version of an API.

.. literalinclude:: ../examples/apig/switch_api_version.py
   :lines: 16-24

Querying the Runtime Definition of an API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the runtime definition
of an API in a specified environment.

.. literalinclude:: ../examples/apig/list_api_runtime_definitions.py
   :lines: 16-24

Querying API Version Details
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the details of a specified API version.

.. literalinclude:: ../examples/apig/list_api_version_details.py
   :lines: 16-23

Taking an API Version Offline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to remove an effective version of an API.

.. literalinclude:: ../examples/apig/offline_api_version.py
   :lines: 16-23

Creating a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to create a signature key.

.. literalinclude:: ../examples/apig/create_signature.py
   :lines: 16-28

Modifying a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to update a signature key.

.. literalinclude:: ../examples/apig/update_signature.py
   :lines: 16-29

Deleting a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to delete a signature key.

.. literalinclude:: ../examples/apig/delete_signature.py
   :lines: 16-23

Querying Signature Keys
^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to fetch all signature keys.

.. literalinclude:: ../examples/apig/list_signatures.py
   :lines: 16-20

Binding a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to bind a signature key.

.. literalinclude:: ../examples/apig/bind_signature.py
   :lines: 16-28

Unbinding a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to unbind a signature key.

.. literalinclude:: ../examples/apig/unbind_signature.py
   :lines: 16-24

Querying Signature Keys Bound to an API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to list the signature keys that
have been bound to a specified API.

.. literalinclude:: ../examples/apig/list_bound_signatures.py
   :lines: 16-24

Querying APIs Not Bound with a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to list the APIs to which a signature key
has not been bound.

.. literalinclude:: ../examples/apig/list_not_bound_apis.py
   :lines: 16-23

Querying APIs Bound with a Signature Key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to list the APIs to which a signature key
has been bound.

.. literalinclude:: ../examples/apig/list_bound_apis.py
   :lines: 16-24

Binding a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to bind request throttling policy to an API.

.. literalinclude:: ../examples/apig/bind_throttling_policy.py
   :lines: 16-28

Unbinding a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to unbind request throttling policy from an API.

.. literalinclude:: ../examples/apig/unbind_throttling_policy.py
   :lines: 16-24

Querying APIs Bound with a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the APIs to which a
specified request throttling policy has been bound.

.. literalinclude:: ../examples/apig/list_bound_throttling_policy_apis.py
   :lines: 16-23

Querying APIs Not Bound with a Request Throttling Policy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the self-developed APIs
to which a request throttling policy has not been bound.
Only published APIs will be displayed.

.. literalinclude:: ../examples/apig/list_not_bound_throttling_policy_apis.py
   :lines: 16-23

Querying Request Throttling Policies Bound to an API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query the request throttling policies
that have been bound to an API.
Only one request throttling policy can be bound to an API in an environment

.. literalinclude:: ../examples/apig/list_bound_throttling_policies.py
   :lines: 16-24

Querying Request Throttling Policies Bound to an API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to unbind request throttling policies from APIs.

.. literalinclude:: ../examples/apig/unbind_throttling_policies.py
   :lines: 16-27

Creating an Excluded Request Throttling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to create an
excluded request throttling configuration.

.. literalinclude:: ../examples/apig/create_throttling_exclude.py
   :lines: 16-50

Modifying an Excluded Request Throttling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to update an
excluded request throttling configuration.

.. literalinclude:: ../examples/apig/update_throttling_exclude.py
   :lines: 16-28

Deleting an Excluded Request Throttling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to delete an
excluded request throttling configuration.

.. literalinclude:: ../examples/apig/delete_throttling_exclude.py
   :lines: 16-24

Querying Excluded Request Throttling Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to query an
excluded request throttling configurations.

.. literalinclude:: ../examples/apig/list_throttling_exclude.py
   :lines: 16-23