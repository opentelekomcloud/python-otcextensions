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

   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.groups
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.get_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.find_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.create_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.delete_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.resume_group
   .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.pause_group


Config Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.configs
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.get_config
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.find_config
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.create_config
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.delete_config
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.batch_delete_configs


Policy Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.policies
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.get_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.find_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.create_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.delete_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.update_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.resume_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.pause_policy
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.execute_policy

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.instances
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.remove_instance
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.batch_instance_action

Actions and Quotas
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy

  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.activities
  .. automethod:: otcextensions.sdk.auto_scaling.v1._proxy.Proxy.quotas
