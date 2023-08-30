Data Ingestion Service (DIS)
============================

Data Ingestion Service (DIS) addresses the challenge of transmitting
data from outside the cloud to inside the cloud. DIS builds data intake
streams for custom applications capable of processing or analyzing streaming
data. DIS continuously captures, transmits, and stores terabytes of data from
hundreds of thousands of sources every hour, such as logs, social media feeds,
website clickstreams, and location-tracking events.

.. contents:: Table of Contents
   :local:

DIS Stream
----------

List DIS Streams
^^^^^^^^^^^^^^^^

This interface is used to query DIS stream list.
:class:`~otcextensions.sdk.dis.v2.stream.Stream`.

.. literalinclude:: ../examples/dis/list_streams.py
   :lines: 16-22

Create DIS Stream
^^^^^^^^^^^^^^^^^^

This interface is used to create a DIS stream with
parameters.
:class:`~otcextensions.sdk.dis.v2.stream.Stream`.

.. literalinclude:: ../examples/dis/create_stream.py
   :lines: 16-27

Get DIS Stream
^^^^^^^^^^^^^^^

This interface is used to get a DIS stream by
stream name.
:class:`~otcextensions.sdk.dis.v2.stream.Stream`.

.. literalinclude:: ../examples/dis/get_stream.py
   :lines: 16-23

Delete DIS Stream
^^^^^^^^^^^^^^^^^^

This interface is used to delete a DIS Stream by
Stream name.
:class:`~otcextensions.sdk.dis.v2.stream.Stream`.

.. literalinclude:: ../examples/dis/delete_stream.py
   :lines: 16-22

Update DIS Stream Partition Count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update partition count
of an existing DIS stream.
:class:`~otcextensions.sdk.dis.v2.stream.Stream`.

.. literalinclude:: ../examples/dis/update_stream_partition.py
   :lines: 16-24


DIS Consumption App
-------------------


List Consumption Apps
^^^^^^^^^^^^^^^^^^^^^

This interface is used to query list of DIS consumption apps.
:class:`~otcextensions.sdk.dis.v2.app.App`.

.. literalinclude:: ../examples/dis/list_apps.py
   :lines: 16-22

Get Consumption App
^^^^^^^^^^^^^^^^^^^

This interface is used to query consumption app
by app name..
:class:`~otcextensions.sdk.dis.v2.stream.Stream`.

.. literalinclude:: ../examples/dis/get_app.py
   :lines: 16-23

Create Consumption App
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a consumption app
with provided parameters.
:class:`~otcextensions.sdk.dis.v2.app.App`.

.. literalinclude:: ../examples/dis/create_app.py
   :lines: 16-25

Delete Consumption App
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a consumption app by
app name.
:class:`~otcextensions.sdk.dis.v2.app.App`.

.. literalinclude:: ../examples/dis/delete_app.py
   :lines: 16-22

List App Consumptions
^^^^^^^^^^^^^^^^^^^^^

This interface is list of app consumptions..
:class:`~otcextensions.sdk.dis.v2.app.App`.

.. literalinclude:: ../examples/dis/list_app_consumptions.py
   :lines: 16-25

DIS Dump Task
-------------

List Dump Tasks
^^^^^^^^^^^^^^^

This interface is used to query list of DIS Dump Tasks.
:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`.

.. literalinclude:: ../examples/dis/list_dump_tasks.py
   :lines: 16-24

Create Dump Task
^^^^^^^^^^^^^^^^

This interface is used to create a DIS Dump Task with
parameters.
:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`.

.. literalinclude:: ../examples/dis/create_dump_task.py
   :lines: 16-37

Get Dump Task
^^^^^^^^^^^^^

This interface is used to get a DIS Stream Dump Task by
task name.
:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`.

.. literalinclude:: ../examples/dis/get_dump_task.py
   :lines: 16-24

Delete Dump Task
^^^^^^^^^^^^^^^^

This interface is used to delete a DIS Stream dump task by
task name.
:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`.

.. literalinclude:: ../examples/dis/delete_dump_task.py
   :lines: 16-23

Start Dump Task
^^^^^^^^^^^^^^^

This interface is used to start DIS Stream dump task.
:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`.

.. literalinclude:: ../examples/dis/start_dump_task.py
   :lines: 16-23

Pause Dump Task
^^^^^^^^^^^^^^^

This interface is used to pause DIS Stream dump task.
:class:`~otcextensions.sdk.dis.v2.dump_task.DumpTask`.

.. literalinclude:: ../examples/dis/pause_dump_task.py
   :lines: 16-23

Data Management
---------------

Upload Data
^^^^^^^^^^^

This interface is used to upload data to DIS Stream.
:class:`~otcextensions.sdk.dis.v2.data.Data`.

.. literalinclude:: ../examples/dis/upload_data.py
   :lines: 16-33

Download Data
^^^^^^^^^^^^^

This interface is used to download data from DIS Stream.
:class:`~otcextensions.sdk.dis.v2.data.Data`.

.. literalinclude:: ../examples/dis/download_data.py
   :lines: 16-27
