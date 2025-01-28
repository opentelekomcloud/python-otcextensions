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
