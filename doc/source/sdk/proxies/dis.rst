DIS API
=======

.. automodule:: otcextensions.sdk.dis.v2._proxy

The Data Ingestion Service Class
--------------------------------

The dis high-level interface is available through the ``dis``
member of a :class:`~openstack.connection.Connection` object.  The
``dis`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

App Operations
^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dis.v2._proxy.Proxy
  :noindex:
  :members: apps, get_app, create_app, app_consumptions,
            delete_app

Checkpoint Operations
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dis.v2._proxy.Proxy
  :noindex:
  :members: create_checkpoint, get_checkpoint, delete_checkpoint

Data Operations
^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dis.v2._proxy.Proxy
  :noindex:
  :members: upload_data, download_data, get_data_cursor

Dump Task Operations
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dis.v2._proxy.Proxy
  :noindex:
  :members: dump_tasks, create_dump_task, get_dump_task,
            start_dump_task, pause_dump_task, delete_dump_task

Stream Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.dis.v2._proxy.Proxy
  :noindex:
  :members: streams, get_stream, create_stream, update_stream_partition,
            delete_stream
