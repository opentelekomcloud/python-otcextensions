FunctionGraph Service (FGS)
===========================

.. contents:: Table of Contents
   :local:

FunctionGraph hosts and computes event-driven functions in a serverless
context while ensuring high availability, high scalability,
and zero maintenance. All you need to do is write your code and set conditions.

Function
--------

Function is a combination of code, runtime, resources,
and settings required to achieve a specific purpose.
It is the minimum unit that can run independently.
A function can be triggered by triggers and automatically schedule
required resources and environments to achieve expected results.


Create Function
^^^^^^^^^^^^^^^

This API is used to create a function.

.. literalinclude:: ../examples/function_graph/create_function.py
   :lines: 16-32

Delete Function
^^^^^^^^^^^^^^^

This API is used to delete a function.

.. literalinclude:: ../examples/function_graph/delete_function.py
   :lines: 16-33

List Functions
^^^^^^^^^^^^^^

This API is used to query all functions.

.. literalinclude:: ../examples/function_graph/list_functions.py
   :lines: 16-24

Get Function Code
^^^^^^^^^^^^^^^^^

This API is used to query the code of a function.

.. literalinclude:: ../examples/function_graph/get_function_code.py
   :lines: 16-23

Get Function Metadata
^^^^^^^^^^^^^^^^^^^^^

This API is used to query the metadata of a function.

.. literalinclude:: ../examples/function_graph/get_function_metadata.py
   :lines: 16-23

Get Resource Tags
^^^^^^^^^^^^^^^^^

This API is used to query resource tags.

.. literalinclude:: ../examples/function_graph/get_resource_tags.py
   :lines: 16-23

Create Resource Tags
^^^^^^^^^^^^^^^^^^^^

This API is used to create resource tags.

.. literalinclude:: ../examples/function_graph/create_resource_tags.py
   :lines: 16-36

Delete Resource Tags
^^^^^^^^^^^^^^^^^^^^

This API is used to delete resource tags.

.. literalinclude:: ../examples/function_graph/delete_resource_tags.py
   :lines: 16-31

Update Function Code
^^^^^^^^^^^^^^^^^^^^

This API is used to modify the code of a function.

.. literalinclude:: ../examples/function_graph/update_function_code.py
   :lines: 16-37

Update Function Metadata
^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to modify the metadata of a function.

.. literalinclude:: ../examples/function_graph/update_function_metadata.py
   :lines: 16-35

Update Function Instances
^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to update the maximum number of instances of a function.

.. literalinclude:: ../examples/function_graph/update_function_metadata.py
   :lines: 16-23

Function Execution Synchronously
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to execute a function synchronously.

.. literalinclude:: ../examples/function_graph/sync_function_invocation.py
   :lines: 16-27

Function Execution Asynchronously
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to execute a function synchronously.

.. literalinclude:: ../examples/function_graph/async_function_invocation.py
   :lines: 16-27

Querying Tenant Quotas
^^^^^^^^^^^^^^^^^^^^^^

This API is used to query tenant quotas.

.. literalinclude:: ../examples/function_graph/list_quotas.py
   :lines: 16-24

Querying Dependencies
^^^^^^^^^^^^^^^^^^^^^

This API is used to query all dependencies.

.. literalinclude:: ../examples/function_graph/list_dependencies.py
   :lines: 16-24

Creating a Dependency Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to create a dependency version.

.. literalinclude:: ../examples/function_graph/delete_dependency_version.py
   :lines: 16-31

Querying Dependency Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query dependency versions.

.. literalinclude:: ../examples/function_graph/list_dependency_versions.py
   :lines: 16-32

Querying a Dependency Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the details about a dependency version.

.. literalinclude:: ../examples/function_graph/get_dependency_version.py
   :lines: 16-31

Deleting a Dependency Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to delete a dependency version.

.. literalinclude:: ../examples/function_graph/delete_dependency_version.py
   :lines: 16-31
