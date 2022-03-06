SDRS API
========

.. automodule:: otcextensions.sdk.sdrs.v1._proxy

The Storage Disaster Recovery Service Class
-------------------------------------------

The SDRS high-level interface is available through the ``sdrs`` member of a
:class:`~openstack.connection.Connection` object.  The ``sdrs`` member will only
be added if the ``otcextensions.sdk.register_otc_extensions(conn)`` method is
called.

Job Operations
^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sdrs.v1._proxy.Proxy
  :noindex:
  :members: get_job

Active-active domains Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sdrs.v1._proxy.Proxy
  :noindex:
  :members: get_domains

Protection group Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sdrs.v1._proxy.Proxy
  :noindex:
  :members: create_protection_group, protection_groups, get_protection_group,
            delete_protection_group, find_protection_group,
            update_protection_group, enable_protection, disable_protection,
            perform_failover, perform_planned_failover

Protected instance Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sdrs.v1._proxy.Proxy
  :noindex:
  :members: create_protected_instance, delete_protected_instance, protected_instances,
            get_protected_instance, update_protected_instance, find_protected_instance,
            attach_replication_pair, detach_replication_pair, add_nic,
            delete_nic, modify_protected_instance

Replication pair Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sdrs.v1._proxy.Proxy
  :noindex:
  :members: create_replication_pair, delete_replication_pair, replication_pairs,
            get_replication_pair, find_replication_pair, expand_replication_pair,
            update_replication_pair

Disaster Recovery drill Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.sdrs.v1._proxy.Proxy
  :noindex:
  :members: create_dr_drill, delete_dr_drill, dr_drills,
            get_dr_drill, find_dr_drill, update_dr_drill