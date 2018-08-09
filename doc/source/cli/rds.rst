==========================================
Database service (rds) command-line client
==========================================

The RDS client is the command-line interface (CLI) for
the Database service (RDS) API and its extensions.

For help on a specific `rds` command, enter:

.. code-block:: console

   $ openstack rds help SUBCOMMAND

.. _datastore:

Datastore operations
--------------------

.. autoprogram-cliff:: openstack.rds.v1
   :command: rds datastore *

.. _flavor:

Flavor operations
-----------------

.. autoprogram-cliff:: openstack.rds.v1
   :command: rds flavor *

.. _instance:

Instance operations
-------------------

.. autoprogram-cliff:: openstack.rds.v1
   :command: rds instance *

.. _backup:

Backup operations
-----------------

.. autoprogram-cliff:: openstack.rds.v1
   :command: rds backup *
