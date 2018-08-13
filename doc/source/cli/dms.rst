=====================================================
Distributed Message Service (DMS) command-line client
=====================================================

The DMS client is the command-line interface (CLI) for
the Distributed Message Service (DMS) API and its extensions.

For help on a specific `dms` command, enter:

.. code-block:: console

   $ openstack dms help SUBCOMMAND

.. _dms_queue:

Queue operations
----------------

.. autoprogram-cliff:: openstack.dms.v1
   :command: dms queue *

.. _dms_group:

Group operations
----------------

.. autoprogram-cliff:: openstack.dms.v1
   :command: dms group *

.. _dms_quota:

Quota operations
----------------

.. autoprogram-cliff:: openstack.dms.v1
   :command: dms quota *
