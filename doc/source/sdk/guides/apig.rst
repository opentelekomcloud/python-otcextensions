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
   :lines: 16-26


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
