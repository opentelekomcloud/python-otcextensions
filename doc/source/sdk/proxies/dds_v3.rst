Document Database (DDS) API
===========================

For details on how to use dds, see /sdk/guides/dds (NEEDS TO BE DONE)

.. automodule:: otcextensions.sdk.dds.v3._proxy

The DDS Class
-------------

The dds high-level interface is available through the ``dds`` member of a
:class:`~openstack.connection.Connection` object.  The ``dds`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Datastore Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: datastores, datastore_types

Flavor Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: flavors

Instance Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: create_instance, delete_instance, get_instance,
            find_instance, instances, restart_instance,
            enlarge_instance, add_instance_nodes, resize_instance,
            switchover_instance, enable_instance_ssl,
            change_instance_name, change_instance_port,
            change_instance_security_group,
            change_instance_private_ip, create_instance_ip,
            configure_client_network, wait_normal_instance

Job Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: get_job, wait_job


Eip Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: bind_eip, unbind_eip

Recycle Bin Policy Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: get_policy, create_policy

Recycle Instances Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dds.v3._proxy.Proxy
  :noindex:
  :members: recycle_instances