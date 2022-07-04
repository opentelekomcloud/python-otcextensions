MapReduce Service (MRS)
=======================

MapReduce Service (MRS) provides enterprise-level big data
clusters on the cloud. Tenants can fully control the clusters
and easily run big data components such as Hadoop, Spark,
HBase, Kafka, and Storm in the clusters.

.. contents:: Table of Contents
   :local:

Cluster
-------

MRS cluster management.

List MRS Clusters
^^^^^^^^^^^^^^^^^

This interface is used to query a list of clusters created by a user.

.. literalinclude:: ../examples/mrs/list_clusters.py
   :lines: 16-22

Get MRS Cluster
^^^^^^^^^^^^^^^

This interface is used to get a MRS Cluster by ID or an instance of
class :class:`~otcextensions.sdk.mrs.v1.cluster.ClusterInfo`.

.. literalinclude:: ../examples/mrs/get_cluster.py
   :lines: 16-23

Find MRS Cluster
^^^^^^^^^^^^^^^^

This interface is used to find a MRS cluster by name or ID. The return value
is a instance of class
:class:`~otcextensions.sdk.mrs.v1.cluster.ClusterInfo`.

.. literalinclude:: ../examples/mrs/find_cluster.py
   :lines: 16-23

Update MRS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to update a MRS Cluster instance with
parameters.

.. literalinclude:: ../examples/mrs/update_cluster.py
   :lines: 16-34

Delete MRS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to delete a MRS Cluster instance by id
or an instance of class
:class:`~otcextensions.sdk.mrs.v1.cluster.Cluster`.

.. literalinclude:: ../examples/mrs/delete_cluster.py
   :lines: 16-23

List MRS Cluster Hosts
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query a list of cluster hosts created by a user.

.. literalinclude:: ../examples/mrs/list_hosts.py
   :lines: 16-22

Datasources
-----------


List MRS Datasources
^^^^^^^^^^^^^^^^^^^^

This interface is used to query MRS Datasources and to filter
the output with query parameters.

.. literalinclude:: ../examples/mrs/list_datasources.py
   :lines: 16-22

Get MRS Datasource
^^^^^^^^^^^^^^^^^^

This interface is used to get a MRS Datasource by ID or an instance of
class :class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`.

.. literalinclude:: ../examples/mrs/get_datasource.py
   :lines: 16-23

Create MRS Datasource
^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a MRS Datasource instance with
parameters.

.. literalinclude:: ../examples/mrs/create_datasource.py
   :lines: 16-31

Update MRS Datasource
^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a MRS Datasource instance with
parameters.

.. literalinclude:: ../examples/mrs/update_datasource.py
   :lines: 16-34

Delete MRS Datasource
^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a MRS Datasource instance by id
or an instance of class
:class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`.

.. literalinclude:: ../examples/mrs/delete_datasource.py
   :lines: 16-23

Find MRS Datasource
^^^^^^^^^^^^^^^^^^^

This interface is used to find a MRS Datasource by name or ID. The return value
is a instance of class
:class:`~otcextensions.sdk.mrs.v1.datasource.Datasource`.

.. literalinclude:: ../examples/mrs/find_datasource.py
   :lines: 16-23

Job binaries
------------

List MRS Job binaries
^^^^^^^^^^^^^^^^^^^^^

This interface is used to query MRS Job binaries and to filter
the output with query parameters.

.. literalinclude:: ../examples/mrs/list_jobbinaries.py
   :lines: 16-22

Get MRS Job binary
^^^^^^^^^^^^^^^^^^

This interface is used to get a MRS Job binary by ID or an instance of
class :class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`.

.. literalinclude:: ../examples/mrs/get_jobbinary.py
   :lines: 16-23

Create MRS Job binary
^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a MRS Job binary instance with
parameters.

.. literalinclude:: ../examples/mrs/create_jobbinary.py
   :lines: 16-30

Update MRS Job binary
^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a MRS Job binary instance with
parameters.

.. literalinclude:: ../examples/mrs/update_jobbinary.py
   :lines: 16-30

Delete MRS Job binary
^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a MRS Job binary instance by id
or an instance of class
:class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`.

.. literalinclude:: ../examples/mrs/delete_jobbinary.py
   :lines: 16-23

Find MRS Job binary
^^^^^^^^^^^^^^^^^^^

This interface is used to find a MRS Job binary by name or ID. The return value
is a instance of class
:class:`~otcextensions.sdk.mrs.v1.jobbinary.Jobbinary`.

.. literalinclude:: ../examples/mrs/find_jobbinary.py
   :lines: 16-23

Job
---

List MRS Job
^^^^^^^^^^^^

This interface is used to query MRS Job and to filter
the output with query parameters.

.. literalinclude:: ../examples/mrs/list_jobs.py
   :lines: 16-22

Get MRS Job
^^^^^^^^^^^

This interface is used to get a MRS Job by ID or an instance of
class :class:`~otcextensions.sdk.mrs.v1.job.Job`.

.. literalinclude:: ../examples/mrs/get_job.py
   :lines: 16-23

Create MRS Job
^^^^^^^^^^^^^^

This interface is used to create a MRS Job instance with
parameters.

.. literalinclude:: ../examples/mrs/create_job.py
   :lines: 16-35

Update MRS Job
^^^^^^^^^^^^^^

This interface is used to update a MRS Job instance with
parameters.

.. literalinclude:: ../examples/mrs/update_job.py
   :lines: 16-37

Delete MRS Job
^^^^^^^^^^^^^^

This interface is used to delete a MRS Job instance by id
or an instance of class
:class:`~otcextensions.sdk.mrs.v1.job.Job`.

.. literalinclude:: ../examples/mrs/delete_job.py
   :lines: 16-23

Find MRS Job
^^^^^^^^^^^^

This interface is used to find a MRS Job by name or ID. The return value
is a instance of class
:class:`~otcextensions.sdk.mrs.v1.job.Job`.

.. literalinclude:: ../examples/mrs/find_job.py
   :lines: 16-23
