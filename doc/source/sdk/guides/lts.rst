Log Tank Service (LTS)
======================

Log Tank Service (LTS) enables you to collect logs from hosts and cloud
services for centralized management, and analyze large volumes of logs
efficiently, securely, and in real time. LTS provides you with the
insights for optimizing the availability and performance of cloud
services and applications. It allows you to make faster data-driven
decisions, perform device O&M with ease, and analyze service trends.

.. contents:: Table of Contents
   :local:

LTS Group
---------

A log group is the basic unit for LTS to manage logs.
You can query and transfer logs in log groups.
Up to 100 log groups can be created in your account.

Groups
^^^^^^

This interface is used to get a list of groups.
:class:`~otcextensions.sdk.lts.v2.group.Group`.

.. literalinclude:: ../examples/lts/list_log_group.py
   :lines: 16-24

Create group
^^^^^^^^^^^^

This interface is used to create new group.
:class:`~otcextensions.sdk.lts.v2.group.Group`.

.. literalinclude:: ../examples/lts/create_log_group.py
   :lines: 16-27

Update group
^^^^^^^^^^^^

This interface is used to update group.
:class:`~otcextensions.sdk.lts.v2.group.Group`.

.. literalinclude:: ../examples/lts/update_log_group.py
   :lines: 16-27

Delete group
^^^^^^^^^^^^

This interface is used to delete group.
:class:`~otcextensions.sdk.lts.v2.group.Group`.

.. literalinclude:: ../examples/lts/delete_log_group.py
   :lines: 16-23


LTS Stream
----------

Up to 100 streams can be created in a log group.

You can separate logs into different log streams based on log types, and name
log streams in an easily identifiable way. This helps you quickly
find your desired logs.

Streams
^^^^^^^

This interface is used to get a list of streams in the group.
:class:`~otcextensions.sdk.lts.v2.stream.Stream`.

.. literalinclude:: ../examples/lts/list_log_stream.py
   :lines: 16-24

Create stream
^^^^^^^^^^^^^

This interface is used to create a stream.
:class:`~otcextensions.sdk.lts.v2.stream.Stream`.

.. literalinclude:: ../examples/lts/create_log_stream.py
   :lines: 16-28

Delete stream
^^^^^^^^^^^^^

This interface is used to delete a stream.
:class:`~otcextensions.sdk.lts.v2.stream.Stream`.

.. literalinclude:: ../examples/lts/delete_log_stream.py
   :lines: 16-24
