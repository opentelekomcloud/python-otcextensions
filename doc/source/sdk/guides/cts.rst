Cloud Trace Service (CTS)
=========================

Cloud Trace is an effective monitoring tool that allows users to analyze
their cloud resources using traces. A tracker is automatically generated when
the service is started. This tracker monitors access to all the respective
user’s cloud resources by means of the traces generated. The monitoring logs
can be saved in the object storage cost-effectively and in the long term. The
Cloud Trace service can also be used in conjunction with Simple Message
Notification, with the user receiving a message when certain events occur.
Cloud Trace is free of charge.

.. contents:: Table of Contents
   :local:

CTS Tracker
-----------

A tracker will be automatically created after CTS is enabled. All traces
recorded by CTS are associated with the tracker. Only one
management tracker is currently created for each account in a region.
On the management console, you can query the last seven days of operation
records. To obtain more operation records, you can enable Object Storage
Service (OBS) and deliver operation records to OBS buckets for long-term
storage in real time.

Create Tracker
^^^^^^^^^^^^^^

This interface is used to create a CTS Tracker instance with parameters.

.. literalinclude:: ../examples/cts/create_tracker.py
   :lines: 16-36

Get Tracker
^^^^^^^^^^^

This interface is used to get a CTS Tracker by name or ID or an instance of
class :class:`~otcextensions.sdk.cts.v1.tracker.Tracker`.

.. literalinclude:: ../examples/cts/get_tracker.py
   :lines: 16-24

Delete Tracker
^^^^^^^^^^^^^^

This interface is used to delete a CTS Tracker instance by id
or an instance of class
:class:`~otcextensions.sdk.cts.v1.tracker.Tracker`.

.. literalinclude:: ../examples/cts/delete_tracker.py
   :lines: 16-22

Update Tracker
^^^^^^^^^^^^^^

This interface is used to update a CTS Tracker instance by
using name or an instance of class
:class:`~otcextensions.sdk.cts.v1.tracker.Tracker` and provide new
attributes.

.. literalinclude:: ../examples/cts/update_tracker.py
   :lines: 16-39


CTS Traces
----------

Traces are the messuremant values of a CTS Tracker.

List Traces
^^^^^^^^^^^

This interface is used to query all CTS Traces of a CTS tracker and to filter
the output with query parameters.

.. literalinclude:: ../examples/cts/list_traces.py
   :lines: 16-26
