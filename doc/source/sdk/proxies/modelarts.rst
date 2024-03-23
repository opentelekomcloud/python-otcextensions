Modelarts API
=============

.. automodule:: otcextensions.sdk.modelartsv1.v1._proxy

The ModelartsV1 Service Class
-----------------------------

The modelarts high-level interface is available through the ``modelartsv1``
member of a :class:`~openstack.connection.Connection` object.  The
``modelartsv1`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Devenv Operations
^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: devenv_instances, find_devenv_instance, get_devenv_instance,
            create_devenv_instance, update_devenv_instance,
            start_devenv_instance, stop_devenv_instance,
            delete_devenv_instance

Built-In Model Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: builtin_models, find_builtin_model

Model Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: models, create_model, find_model, get_model, delete_model

Service Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: services, create_service, find_service, get_service,
            update_service, start_service, stop_service, delete_service,
            service_logs, service_events, service_monitor, service_flavors,
            service_clusters

Training Job Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: training_jobs, create_training_job, find_training_job,
            update_training_job, delete_training_job

Training Job Config Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: training_job_configs, create_training_job_config,
            get_training_job_config, delete_training_job_config,
            update_training_job_config

Training Job Version Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: training_job_versions, create_training_job_version,
            get_training_job_version, delete_training_job_version,
            stop_training_job_version

Visualization Job Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv1.v1._proxy.Proxy
  :noindex:
  :members: visualization_jobs, create_visualization_job,
            get_visualization_job, delete_visualization_job,
            update_visualization_job, stop_visualization_job,
            restart_visualization_job

The ModelartsV2 Service Class
-----------------------------

The modelarts high-level interface is available through the ``modelartsv2``
member of a :class:`~openstack.connection.Connection` object.  The
``modelartsv2`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Dataset Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: datasets, find_dataset, get_dataset, create_dataset,
            update_dataset, delete_dataset

Dataset Label Operations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: dataset_labels, create_dataset_label, update_dataset_labels,
            delete_dataset_labels

Dataset Version Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: dataset_versions, create_dataset_version,
            get_dataset_version, delete_dataset_labels

Dataset Sample Operations
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: dataset_samples, add_dataset_samples,
            get_dataset_sample, delete_dataset_samples

Dataset Import Task Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: dataset_import_tasks, create_dataset_import_task,
            get_dataset_import_task

Dataset Export Task Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: dataset_export_tasks, create_dataset_export_task,
            get_dataset_export_task

Dataset Sync Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.modelartsv2.v2._proxy.Proxy
  :noindex:
  :members: dataset_sync, get_dataset_sync_status
