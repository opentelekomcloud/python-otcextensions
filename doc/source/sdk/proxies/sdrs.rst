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