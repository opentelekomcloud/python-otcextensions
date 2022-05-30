Cloud Backup and Recovery (CBR)
===============================

The CBR client is the command-line interface (CLI) for
the Cloud Backup and Recovery (CBR) API and its extensions.

For help on a specific `cbr` command, enter:

.. code-block:: console

   $ openstack cbr help SUBCOMMAND

.. _cbr_backup:

Backup operations
-----------------

.. autoprogram-cliff:: openstack.cbr.v3
   :command: cbr backup *

.. _cbr_checkpoint:

Checkpoint operations
---------------------

.. autoprogram-cliff:: openstack.cbr.v3
   :command: cbr checkpoint *

.. _cbr_policy:

Policy operations
-----------------

.. autoprogram-cliff:: openstack.cbr.v3
   :command: cbr policy *

.. _cbr_task:

Task operations
-----------------

.. autoprogram-cliff:: openstack.cbr.v3
   :command: cbr task *

.. _cbr_vault:

Vault operations
-----------------

.. autoprogram-cliff:: openstack.cbr.v3
   :command: cbr vault *
