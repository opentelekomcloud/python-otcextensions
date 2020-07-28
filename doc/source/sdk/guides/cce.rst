Cloud Container Engine (CCE)
============================

.. contents:: Table of Contents
   :local:

CCE Cluster
-----------

Cloud Container Engine (CCE) is a highly reliable and high-performance service
that allows enterprises to manage containerized applications. With support
for Kubernetes-native applications and tools, CCE makes it simple to set up
an environment for running containers in the cloud. CCE Clusters are the
environment where cluster nodes are administrated. The core component
is a Kubernetes Cluster with advanced features.

List CCE Clusters
^^^^^^^^^^^^^^^^^

This interface is used to query all CCE clusters and to filter
the output with query parameters.

.. literalinclude:: ../examples/cce/list_clusters.py
   :lines: 16-22

Create CCE Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to create a CCE cluster instance with
parameters.

.. literalinclude:: ../examples/cce/create_cluster.py
   :lines: 16-53

Get CCE Cluster
^^^^^^^^^^^^^^^

This interface is used to get a CCE cluster by ID
or an instance of class
:class:`~otcextensions.sdk.cce.v3.cluster.Cluster`.

.. literalinclude:: ../examples/cce/get_cluster.py
   :lines: 16-24

Find CCE Cluster
^^^^^^^^^^^^^^^^

This interface is used to find a CCE cluster by ID
or name.

.. literalinclude:: ../examples/cce/find_cluster.py
   :lines: 16-24

Delete CCE Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to get a CCE cluster by ID
or an instance of class
:class:`~otcextensions.sdk.cce.v3.cluster.Cluster`.

.. literalinclude:: ../examples/cce/delete_cluster.py
   :lines: 16-25

CCE Node
--------

A CCE cluster node is the computing instance of a CCE cluster where
containers are hosted. One cluster can manage several nodes which
can be distributed over different availability zones to increase
reliability.

List CCE Cluster Nodes
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all nodes of a CCE cluster
and to filter the output with query parameters.

.. literalinclude:: ../examples/cce/list_cluster_nodes.py
   :lines: 16-25

Create CCE Cluster Node
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a CCE cluster node instance with
parameters.

.. literalinclude:: ../examples/cce/create_cluster_node.py
   :lines: 16-53

Get CCE Cluster Node
^^^^^^^^^^^^^^^^^^^^

This interface is used to get a CCE cluster by ID
or an instance of class
:class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`.

.. literalinclude:: ../examples/cce/get_cluster_node.py
   :lines: 16-26

Find CCE Cluster Node
^^^^^^^^^^^^^^^^^^^^^

This interface is used to find a node of a CCE cluster by ID
or name.

.. literalinclude:: ../examples/cce/find_cluster_node.py
   :lines: 16-26

Delete CCE Cluster Node
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a CCE cluster node by ID
or an instance of class
:class:`~otcextensions.sdk.cce.v3.cluster_node.ClusterNode`.

.. literalinclude:: ../examples/cce/delete_cluster_node.py
   :lines: 16-25

Job Operations
--------------

Jobs are created while cluster creation and other similar operations
have been started. Jobs have different phases and can be triggered by
the following methods.

Get Job
^^^^^^^

This interface is used to get a CCE Job by ID
or an instance of class
:class:`~otcextensions.sdk.cce.v3.job.Job`.

.. literalinclude:: ../examples/cce/get_job.py
   :lines: 16-24

Wait for a Job
^^^^^^^^^^^^^^

This interface is used to wait for a CCE Job until reaches a specific state
by using ID or an instance of class
:class:`~otcextensions.sdk.cce.v3.job.Job`.

.. literalinclude:: ../examples/cce/wait_for_job.py
   :lines: 16-24

