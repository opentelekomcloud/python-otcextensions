FunctionGraph API
=================

.. automodule:: otcextensions.sdk.function_graph.v2._proxy

Function Service Class
----------------------

The nat high-level interface is available through the ``functiongraph``
member of a :class:`~openstack.connection.Connection` object.  The
``functiongraph`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Function Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: create_function, delete_function, functions,
            get_function_code, get_function_metadata, get_resource_tags,
            create_resource_tags, delete_resource_tags, update_pin_status,
            update_function_code, update_function_metadata, update_max_instances

Function Invocation Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: executing_function_synchronously, executing_function_asynchronously

Function Quotas
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: quotas

Dependencies
^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: dependencies, create_dependency_version, delete_dependency_version,
            dependency_versions, get_dependency_version

Events
^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: create_event, delete_event, events,
            get_event, update_event

Versions
^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: versions, publish_version

Aliases
^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: aliases, create_alias, delete_alias,
            update_alias, get_alias


Metrics
^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: metrics, function_metrics

Logs
^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: get_lts_log_settings, enable_lts_log

Templates
^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: get_template

Reserved Instances
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: update_instances_number, reserved_instances_config,
            reserved_instances


Export
^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: export_function

Import
^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: import_function

Function Triggers
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.function_graph.v2._proxy.Proxy
  :noindex:
  :members: create_trigger, delete_trigger, delete_all_triggers,
            triggers, get_trigger, update_trigger
