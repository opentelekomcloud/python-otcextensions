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

Function Lifecycle
------------------

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

Function Invocation
-------------------

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

Function Quotas
---------------

Querying Tenant Quotas
^^^^^^^^^^^^^^^^^^^^^^

This API is used to query tenant quotas.

.. literalinclude:: ../examples/function_graph/list_quotas.py
   :lines: 16-24

Dependencies
------------

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

Test Events
-----------

Querying Test Events of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the test events of a function.

.. literalinclude:: ../examples/function_graph/list_events.py
   :lines: 16-24

Creating a Test Event
^^^^^^^^^^^^^^^^^^^^^

This API is used to query the test events of a function.

.. literalinclude:: ../examples/function_graph/create_event.py
   :lines: 16-39

Deleting a Test Event
^^^^^^^^^^^^^^^^^^^^^

This API is used to delete a test event.

.. literalinclude:: ../examples/function_graph/delete_event.py
   :lines: 16-40

Obtaining the Details of a Test Event
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the details of a test event.

.. literalinclude:: ../examples/function_graph/get_event.py
   :lines: 16-42

Updating a Test Event
^^^^^^^^^^^^^^^^^^^^^

This API is used to update a test event.

.. literalinclude:: ../examples/function_graph/update_event.py
   :lines: 16-45

Publishing a Function Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to publish a function version.

.. literalinclude:: ../examples/function_graph/publish_version.py
   :lines: 16-41

Querying the Versions of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the versions of a function.

.. literalinclude:: ../examples/function_graph/list_versions.py
   :lines: 16-24

Querying All Aliases of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the versions and aliases of a function.

.. literalinclude:: ../examples/function_graph/list_aliases.py
   :lines: 16-24

Creating an Alias for a Function Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to create an alias for a function version.

.. literalinclude:: ../examples/function_graph/create_alias.py
   :lines: 16-40

Deleting an Alias of a Function Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to delete an alias of a function version.

.. literalinclude:: ../examples/function_graph/delete_alias.py
   :lines: 16-40

Modifying the Alias of a Function Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to modify the alias of a function version.

.. literalinclude:: ../examples/function_graph/update_alias.py
   :lines: 16-47

Querying the Alias of a Function Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the alias of a function version.

.. literalinclude:: ../examples/function_graph/get_alias.py
   :lines: 16-42

Querying Metrics in a Specified Period
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the alias of a function version.

.. literalinclude:: ../examples/function_graph/list_function_metrics.py
   :lines: 16-35

Querying Tenant-Level Function Statistics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the alias of a function version.

.. literalinclude:: ../examples/function_graph/list_metrics.py
   :lines: 16-24

Querying the Log Group and Stream of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the LTS log group and stream settings of a function.

.. literalinclude:: ../examples/function_graph/get_lts_log_detail.py
   :lines: 16-35

Enabling Log Reporting to LTS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to enable log reporting to LTS.

.. literalinclude:: ../examples/function_graph/enable_lts_log.py
   :lines: 16-23

Querying a Specified Function Template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query a specified function template.

.. literalinclude:: ../examples/function_graph/get_template.py
   :lines: 16-26

Querying Reserved Instances of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query reserved instances of a function.

.. literalinclude:: ../examples/function_graph/list_reserved_instances_config.py
   :lines: 16-24

Querying the Number of Reserved Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the number of instances reserved for a function.

.. literalinclude:: ../examples/function_graph/list_reserved_instances.py
   :lines: 16-24

Changing the Number of Reserved Instances
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to change the number of reserved instances.

.. literalinclude:: ../examples/function_graph/update_reserved_instances.py
   :lines: 16-40

Importing a Function
^^^^^^^^^^^^^^^^^^^^

This API is used to import a function.

.. literalinclude:: ../examples/function_graph/import_function.py
   :lines: 16-39

Exporting a Function
^^^^^^^^^^^^^^^^^^^^

This API is used to export a function.

.. literalinclude:: ../examples/function_graph/export_function.py
   :lines: 16-38

Deleting All Triggers of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to delete all triggers of a function.

.. literalinclude:: ../examples/function_graph/delete_all_triggers.py
   :lines: 16-36

Deleting a Trigger
^^^^^^^^^^^^^^^^^^

This API is used to delete a trigger.

.. literalinclude:: ../examples/function_graph/delete_trigger.py
   :lines: 16-50

Querying All Triggers of a Function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query all triggers of a function.

.. literalinclude:: ../examples/function_graph/list_triggers.py
   :lines: 16-24

Creating a Trigger
^^^^^^^^^^^^^^^^^^

This API is used to create a trigger.

.. literalinclude:: ../examples/function_graph/create_trigger.py
   :lines: 16-46

Querying a Trigger
^^^^^^^^^^^^^^^^^^

This API is used to query a specified trigger.

.. literalinclude:: ../examples/function_graph/get_trigger.py
   :lines: 16-50

Updating a Trigger
^^^^^^^^^^^^^^^^^^

This API is used to update a trigger.

.. literalinclude:: ../examples/function_graph/update_trigger.py
   :lines: 16-56

Querying Asynchronous Execution Notification Settings of a Function Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the asynchronous invocation
setting of a function version.

.. literalinclude:: ../examples/function_graph/list_async_notifications.py
   :lines: 16-24

Deleting Asynchronous Execution Notification Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to delete the asynchronous execution
notification settings of a function.

.. literalinclude:: ../examples/function_graph/delete_async_notification.py
   :lines: 16-37

Configuring Asynchronous Execution Notification
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to configure asynchronous execution
notification for a function.

.. literalinclude:: ../examples/function_graph/configure_async_notification.py
   :lines: 16-37

Querying Asynchronous Execution Notification Settings of All Versions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the asynchronous execution notification
settings of a function's all versions.

.. literalinclude:: ../examples/function_graph/list_all_async_notifications.py
   :lines: 16-31

Querying Asynchronous Invocation Requests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the asynchronous invocation requests of a function.

.. literalinclude:: ../examples/function_graph/list_async_invocation_requests.py
   :lines: 16-24

Stopping an Asynchronous Invocation Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to stop asynchronous invocation of a function with
N concurrent instances.
When calling this API, set recursive to false and force to true.
The API will also stop the function's other concurrent requests
and return "4208 function invocation canceled".

.. literalinclude:: ../examples/function_graph/stop_async_invocation_request.py
   :lines: 16-37
