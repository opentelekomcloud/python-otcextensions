AutoScaling API
===============

For details on how to use auto scaling, see /sdk/guides/auto_scaling
(NEEDS TO BE DONE).

.. automodule:: otcextensions.sdk.auto_scaling.v1._proxy

The AutoScaling Class
---------------------

The AS high-level interface is available through the ``auto_scaling``
member of a :class:`~openstack.connection.Connection` object.  The
``auto_scaling`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Group Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy
  :noindex:
  :members: groups, get_group, find_group, create_group, delete_group,
            resume_group, pause_group

Config Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy
  :noindex:
  :members: configs, get_config, find_config, create_config, delete_config,
            batch_delete_configs


Policy Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy
  :noindex:
  :members: policies, get_policy, find_policy, create_policy,
            delete_policy, update_policy, resume_policy,
            pause_policy, execute_policy

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy
  :noindex:
  :members: instances, remove_instance, batch_instance_action

Actions and Quotas
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy
  :noindex:
  :members: activities, quotas
