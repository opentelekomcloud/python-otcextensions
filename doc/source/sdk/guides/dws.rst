Data Warehouse Service (DWS)
============================

GaussDB(DWS) is an online data processing database that runs on the cloud
infrastructure to provide scalable, fully-managed, and out-of-the-box analytic
database service, freeing you from complex database management and monitoring.
It is a native cloud service based on the converged data warehouse GaussDB,
and is fully compatible with the standard ANSI SQL 99 and SQL 2003, as well
as the PostgreSQL and Oracle ecosystems. GaussDB(DWS) provides competitive
solutions for PB-level big data analysis in various industries.

.. contents:: Table of Contents
   :local:

DWS Cluster
-----------

List DWS Clusters
^^^^^^^^^^^^^^^^^

This interface is used to query an DWS cluster list.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/list_clusters.py
   :lines: 16-22

Create DWS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to create a DWS cluster with
parameters.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/create_cluster.py
   :lines: 16-38

Get DWS Cluster
^^^^^^^^^^^^^^^

This interface is used to get details of DWS Cluster by
cluster_id or instance of Cluster class.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/get_cluster.py
   :lines: 16-23

Find DWS Cluster
^^^^^^^^^^^^^^^^

This interface is used to find a DWS cluster by id or name.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/find_cluster.py
   :lines: 16-23

Restart DWS Cluster
^^^^^^^^^^^^^^^^^^^

This interface is used to restart DWS Cluster by cluster
name_or_id or instance of Cluster class.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/restart_cluster.py
   :lines: 16-22

Extend DWS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to scale out nodes of DWS Cluster
by cluster name_or_id or instance of Cluster class.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/extend_cluster.py
   :lines: 17-24

Reset DWS Password
^^^^^^^^^^^^^^^^^^

This interface is used to reset the password of DWS cluster
administrator by cluster name_or_id or instance of Cluster class.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/reset_cluster_password.py
   :lines: 17-24

Delete DWS Cluster
^^^^^^^^^^^^^^^^^^

This interface is used to delete DWS Cluster by cluster name
or id or instance of Cluster class.
:class:`~otcextensions.sdk.dws.v1.cluster.Cluster`.

.. literalinclude:: ../examples/dws/delete_cluster.py
   :lines: 16-22


DWS Cluster Snapshot
--------------------

A GaussDB(DWS) snapshot is a complete backup of a cluster. Snapshots are
stored in the storage space of Object Storage Service (OBS). A snapshot can
be used to restore a cluster to a newly created one that has the same flavor.
Currently, you can only restore a cluster to a new one.

List Snapshots
^^^^^^^^^^^^^^

This interface is used to query all DWS snapshots in a project.
:class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/dws/list_snapshots.py
   :lines: 16-22

Create Snapshot
^^^^^^^^^^^^^^^

This interface is used to manually create snapshots for a specified
DWS cluster.
:class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/dws/create_snapshot.py
   :lines: 16-29

Get Snapshot
^^^^^^^^^^^^

This interface is used to query details of DWS Snapshot by
snapshot_id or instance of Snapshot class.
:class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/dws/get_snapshot.py
   :lines: 16-23

Find Snapshot
^^^^^^^^^^^^^

This interface is used to find a DWS Snapshot by id or name.
:class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/dws/find_snapshot.py
   :lines: 16-23

Restore Snapshot
^^^^^^^^^^^^^^^^

This interface is used to restore snapshot to a DWS cluster to a newly
created one.
:class:`~otcextensions.sdk.dws.v1.snapshot.Restore`.

.. literalinclude:: ../examples/dws/restore_snapshot.py
   :lines: 16-37

Delete Snapshot
^^^^^^^^^^^^^^^

This interface is used to delete a manually created
snapshot of a cluster. This interface requires snapshot
name_or_id or instance of Snapshot class.
:class:`~otcextensions.sdk.dws.v1.snapshot.Snapshot`.

.. literalinclude:: ../examples/dws/delete_snapshot.py
   :lines: 16-22

DWS Flavor
----------

List DWS Flavors
^^^^^^^^^^^^^^^^

This interface is used to query list of node types (flavors)
supported by DWS Cluster.
:class:`~otcextensions.sdk.dws.v1.flavor.Flavor`.

.. literalinclude:: ../examples/dws/list_flavors.py
   :lines: 16-22
