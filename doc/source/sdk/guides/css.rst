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
   :lines: 17-24

Create CSS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to create a CSS cluster with
parameters.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/create_cluster.py
   :lines: 17-56

Get CSS Cluster
^^^^^^^^^^^^^^^

This interface is used to get a CSS cluster by ID
or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/get_cluster.py
   :lines: 17-24

Find CSS Cluster
^^^^^^^^^^^^^^^^

This interface is used to find a CSS cluster by id or name.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/find_cluster.py
   :lines: 17-24

Restart CSS Cluster
^^^^^^^^^^^^^^^^^^^

This interface is used to restart a CSS cluster by
id or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/restart_cluster.py
   :lines: 17-23

Extend CSS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to extend CSS cluster by
id or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/extend_cluster.py
   :lines: 18-25

Extend CSS Cluster Nodes
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to extend CSS cluster nodes by
id or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/extend_cluster_nodes.py
   :lines: 17-30

Delete CSS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to delete a CSS Cluster by ID
or an instance of class
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/delete_cluster.py
   :lines: 17-23

Add CSS Cluster Nodes
^^^^^^^^^^^^^^^^^^^^^

This interface is used to add master and client nodes to a cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/add_cluster_nodes.py
   :lines: 17-33

Create CSS Opensearch Cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create a CSS opensearch cluster with
parameters.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/create_cluster_opensearch.py
   :lines: 17-63

Get CSS Cluster Upgrade Info
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to obtain the CSS cluster updgrade details.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/get_cluster_upgrade_info.py
   :lines: 17-29

Get CSS Cluster Version Upgrade Info
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get the CSS cluster version upgrade info.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/get_cluster_version_upgrade_info.py
   :lines: 17-28

Replace CSS Cluster Node
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to replace a failed node in a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/replace_cluster_node.py
   :lines: 17-27

Retry CSS Cluster Upgrade Job
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to retry a task or terminate the impact
of a task in a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/retry_cluster_upgrade_job.py
   :lines: 17-28

Scale In CSS cluster
^^^^^^^^^^^^^^^^^^^^

This interface is used to scale in a CSS cluster by removing
specified nodes.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.:

.. literalinclude:: ../examples/css/scale_in_cluster.py
   :lines: 17-27

Scale In CSS Cluster By Node Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to remove instances of specific
types and reduce instance storage capacity in a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/scale_in_cluster_by_node_type.py
   :lines: 18-28

Update CSS Cluster Flavor
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update the flavor of a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/update_cluster_flavor.py
   :lines: 17-28

Update CSS Cluster Kernel
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update the kernel of a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/update_cluster_kernel.py
   :lines: 17-40

Update CSS Cluster Name
^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update the name of a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/update_cluster_name.py
   :lines: 17-28

Update CSS Cluster Password
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update the password of a CSS cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/update_cluster_password.py
   :lines: 17-28

Update CSS Cluster Security Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update the security group of a CSS
cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/update_cluster_security_group.py
   :lines: 17-28

Update CSS Cluster Security Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update the security mode of a CSS
cluster.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/update_cluster_security_mode.py
   :lines: 17-31

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
   :lines: 17-24

Find Snapshot
^^^^^^^^^^^^^

This interface is used to find a CSS snapshot by id or name.
:class:`~otcextensions.sdk.css.v1.cluster.Cluster`.

.. literalinclude:: ../examples/css/find_snapshot.py
   :lines: 17-28

Create Snapshot
^^^^^^^^^^^^^^^

This interface is used to manually create a snapshot
by id or an instance of cluster class.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/create_snapshot.py
   :lines: 17-30

Restore Snapshot
^^^^^^^^^^^^^^^^

This interface is used to restore a snapshot with
indices to a target cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/restore_snapshot.py
   :lines: 17-30

Delete Snapshot
^^^^^^^^^^^^^^^

This interface is used to delete a manually created
snapshot of a cluster. This interface requires id or
an instance of cluster class and id of the snapshot.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/delete_snapshot.py
   :lines: 17-24

Set Snapshot Policy
^^^^^^^^^^^^^^^^^^^

This interface is used to set parameters related to
automatic snapshot creation for a cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.SnapshotPolicy`.

.. literalinclude:: ../examples/css/set_snapshot_policy.py
   :lines: 17-31

Get Snapshot Policy
^^^^^^^^^^^^^^^^^^^

This interface is used to query the automatic snapshot
creation policy for a cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.SnapshotPolicy`.

.. literalinclude:: ../examples/css/get_snapshot_policy.py
   :lines: 17-24

Set Snapshot Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to set basic configurations for a
cluster snapshot, including configuring OBS buckets and
IAM agency.
:class:`~otcextensions.sdk.css.v1.snapshot.SnapshotConfiguration`.

.. literalinclude:: ../examples/css/set_snapshot_configuration.py
   :lines: 17-33

Disable Snapshot Function
^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to disable the snapshot function
for a cluster.
:class:`~otcextensions.sdk.css.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/css/disable_snapshot_function.py
   :lines: 17-23
