Cloud Search Service (CSS)
==========================

Cloud Search Service is a fully hosted distributed search service
powered on Elasticsearch. It is fully compatible with Elasticsearch
APIs and provides users with structured and unstructured data search,
statistics, and report capabilities.

.. contents:: Table of Contents
   :local:

CSS Cluster
-----------

List CSS Clusters
^^^^^^^^^^^^^^^^^

This interface is used to query an CSS cluster list..
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/list_clusters.py
   :lines: 16-22

Create CSS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to create a CSS cluster with
parameters.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/create_cluster.py
   :lines: 16-44

Get CSS Cluster
^^^^^^^^^^^^^^^

This interface is used to get a CSS cluster by ID
or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/get_cluster.py
   :lines: 16-23

Find CSS Cluster
^^^^^^^^^^^^^^^^

This interface is used to find a CSS cluster by id or name.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/find_cluster.py
   :lines: 16-24

Restart CSS Cluster
^^^^^^^^^^^^^^^^^^^

This interface is used to restart a CSS cluster by
id or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/restart_cluster.py
   :lines: 16-22

Extend CSS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to extend CSS cluster by
id or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/extend_cluster.py
   :lines: 17-24

Extend CSS Cluster Nodes
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to extend CSS cluster nodes by
id or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/extend_cluster_nodes.py
   :lines: 16-29

Delete CSS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to delete a CSS Cluster by ID
or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/delete_cluster.py
   :lines: 16-22


CSS Cluster Snapshot
--------------------

The SNAT function translates a private IP address to a public IP
address by binding EIPs to servers in a VPC, providing secure and
efficient access to the Internet.

List Snapshots
^^^^^^^^^^^^^^

This interface is used to query all snapshots of a cluster
by id or an instance of cluster class.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/list_snapshots.py
   :lines: 16-23

Create Snapshot
^^^^^^^^^^^^^^^

This interface is used to manually create a snapshot
by id or an instance of cluster class.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/create_snapshot.py
   :lines: 16-29

Restore Snapshot
^^^^^^^^^^^^^^^^

This interface is used to restore a snapshot with
indices to a target cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/restore_snapshot.py
   :lines: 16-29

Delete Snapshot
^^^^^^^^^^^^^^^

This interface is used to delete a manually created
snapshot of a cluster. This interface requires id or
an instance of cluster class and id of the snapshot.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/delete_snapshot.py
   :lines: 16-23

Set Snapshot Policy
^^^^^^^^^^^^^^^^^^^

This interface is used to set parameters related to
automatic snapshot creation for a cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.SnapshotPolicy`.

.. literalinclude:: ../examples/css/set_snapshot_policy.py
   :lines: 16-30

Get Snapshot Policy
^^^^^^^^^^^^^^^^^^^

This interface is used to query the automatic snapshot
creation policy for a cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.SnapshotPolicy`.

.. literalinclude:: ../examples/css/get_snapshot_policy.py
   :lines: 16-23

Set Snapshot Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to set basic configurations for a
cluster snapshot, including configuring OBS buckets and
IAM agency.
:class:`~otcextensions.sdk.css.v1.snapshot.SnapshotConfiguration`.

.. literalinclude:: ../examples/css/set_snapshot_configuration.py
   :lines: 16-31

Disable Snapshot Function
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to disable the snapshot function
for a cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/disable_snapshot_function.py
   :lines: 16-22
