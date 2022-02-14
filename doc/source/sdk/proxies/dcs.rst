DCS API
=======

.. automodule:: otcextensions.sdk.dcs.v1._proxy

The Distributed Cache Service Class
-------------------------------------

The dcs high-level interface is available through the ``dcs``
member of a :class:`~openstack.connection.Connection` object.  The
``dcs`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Instance Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcs.v1._proxy.Proxy
  :noindex:
  :members: instances, get_instance, find_instance, create_instance,
            delete_instance, update_instance, extend_instance,
            start_instance, restart_instance, stop_instance

Statistics Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcs.v1._proxy.Proxy
  :noindex:
  :members: statistics

Backup Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcs.v1._proxy.Proxy
  :noindex:
  :members: backups, backup_instance, delete_instance_backup,
            restore_instance, restore_records

Instance Configuration Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcs.v1._proxy.Proxy
  :noindex:
  :members: instance_params, update_instance_params

Service Specification Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dcs.v1._proxy.Proxy
  :noindex:
  :members: service_specifications
