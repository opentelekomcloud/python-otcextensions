Data Warehouse Service (DWS)
============================

The DWS client is the command-line interface (CLI) for
the Data Warehouse Service (DWS) API and its extensions.

For help on a specific `dws` command, enter:

.. code-block:: console

   $ openstack dws help SUBCOMMAND

.. _dws_cluster:

DWS Cluster Operations
----------------------

.. autoprogram-cliff:: openstack.dws.v1
   :command: dws cluster *

.. _dws_snapshot:

DWS Snapshot Operations
-----------------------

.. autoprogram-cliff:: openstack.dws.v1
   :command: dws snapshot *

.. _dws_flavor:

DWS Flavor Operations
---------------------

.. autoprogram-cliff:: openstack.dws.v1
   :command: dws flavor *
