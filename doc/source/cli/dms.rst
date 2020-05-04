Distributed Message Service (DMS)
=================================

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

.. _dms_instance:

Instance operations
-------------------

.. autoprogram-cliff:: openstack.dms.v1
   :command: dms instance *

.. _dms_misq:

Misc operations
---------------

.. autoprogram-cliff:: openstack.dms.v1
  :command: dms az list

.. autoprogram-cliff:: openstack.dms.v1
  :command: dms maintenance window list

.. autoprogram-cliff:: openstack.dms.v1
  :command: dms product list
