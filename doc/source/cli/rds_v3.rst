Relational Database Service (RDS)
=================================

The RDS client is the command-line interface (CLI) for
the Database service (RDS) API and its extensions.

For help on a specific `rds` command, enter:

.. code-block:: console

   $ openstack rds help SUBCOMMAND

.. _datastore:

Datastore Operations
--------------------

.. autoprogram-cliff:: openstack.rds.v3
   :command: rds datastore *

.. _flavor:

Flavor Operations
-----------------

.. autoprogram-cliff:: openstack.rds.v3
   :command: rds flavor *

.. _instance:

Instance Operations
-------------------

.. autoprogram-cliff:: openstack.rds.v3
   :command: rds instance *

.. _backup:

Backup Operations
-----------------

.. autoprogram-cliff:: openstack.rds.v3
   :command: rds backup *

.. _configuration:

Configuration Operations
------------------------

.. autoprogram-cliff:: openstack.rds.v3
   :command: rds configuration *
