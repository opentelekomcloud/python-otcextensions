Cloud Eye Service (CES)
=========================

Cloud Eye (CES) is a high-performance monitoring service with integrated
alarm functions. Open Telekom Cloud users benefit from a dashboard with
a basic overview of resources and their current status. Users can
configure the alarm function in such a way that they receive
notifications via SMS or email. Monitoring with the Cloud Eye Service
is activated by default; the free service does not need to be booked
or activated.

.. contents:: Table of Contents
   :local:

CES Alarm Rule
--------------

The alarm function is based on collected metrics. You can set alarm rules for
key metrics of cloud services. When the metric data triggers the conditions
set in the alarm rule, Cloud Eye sends emails, or text messages, to you, or
sends HTTP/HTTPS requests to the servers. In this way, you are immediately
informed of cloud service exceptions and can quickly handle the faults to
avoid service losses.

Cloud Eye uses the SMN service to notify users. This
requires you to create a topic and add subscriptions to this topic on the
SMN console first. Then when you create alarm rules, you can enable the
Alarm Notification function and select the created topic. When an error
occurs, Cloud Eye can broadcast alarm information to those subscriptions in
real time.


Create Alarm Rule
^^^^^^^^^^^^^^^^^

This interface is used to create a CES alarm with parameters.

.. literalinclude:: ../examples/ces/create_alarm.py
   :lines: 16-89

Get Alarm Rule
^^^^^^^^^^^^^^

This interface is used to get a CES alarm rule by name or ID or an instance of
class :class:`~otcextensions.sdk.ces.v1.alarm.Alarm`.

.. literalinclude:: ../examples/ces/get_alarm.py
   :lines: 16-24

Delete Alarm Rule
^^^^^^^^^^^^^^^^^

This interface is used to delete a CES Alarm Rule instance by id
or an instance of class
:class:`~otcextensions.sdk.cts.v1.tracker.Tracker`.

.. literalinclude:: ../examples/ces/delete_alarm.py
   :lines: 16-25

Switch Alarm Rule State
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to switch the Alarm Rule State by using name or id.

.. literalinclude:: ../examples/ces/switch_alarm_state.py
   :lines: 16-25


Monitoring Data Management
--------------------------

Monitoring / Metric data is used to generate and query custom monitoring
data.

List Metric Data
^^^^^^^^^^^^^^^^

This interface is used to query all CES metric data and to filter
the output with query parameters.

.. literalinclude:: ../examples/ces/list_metric_data.py
   :lines: 16-34


Miscellaneous
-------------

List Metrics
^^^^^^^^^^^^

This API is used to query the metric list. You can specify the namespace,
metric, dimension, sorting order, start records, and the maximum number of
records when using this API to query metrics.

.. literalinclude:: ../examples/ces/list_metrics.py
   :lines: 16-23

List Quotas
^^^^^^^^^^^

This API is used to query a resource quota and the used amount. The current
resource refers to alarm rules only.

.. literalinclude:: ../examples/ces/list_quotas.py
   :lines: 16-23

List Host Configuration / Event Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This API is used to query the host configuration for a specified event type
in a specified period of time. You can specify the dimension of data to be
queried.

.. literalinclude:: ../examples/ces/list_event_data.py
   :lines: 16-32
