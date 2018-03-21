============================================
AutoScaling service (AS) command-line client
============================================

The AS client is the command-line interface (CLI) for
the AutoScaling service (AS) API and its extensions.

For help on a specific `as` command, enter:

.. code-block:: console

   $ openstack as help SUBCOMMAND

.. _group:

Group operations
----------------

.. autoprogram-cliff:: openstack.auto_scaling.v1
   :command: as group *

.. _config:

Config operations
-----------------

.. autoprogram-cliff:: openstack.auto_scaling.v1
   :command: as configuration *
