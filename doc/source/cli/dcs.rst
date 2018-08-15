===================================================
Distributed Cache Service (DCS) command-line client
===================================================

The DCS client is the command-line interface (CLI) for
the Distributed Cache Service (DMS) API and its extensions.

For help on a specific `dcs` command, enter:

.. code-block:: console

   $ openstack dcs help SUBCOMMAND

.. _dcs_instance:

Instance operations
-------------------

.. autoprogram-cliff:: openstack.dcs.v1
   :command: dcs instance *

.. _dcs_stat:

Statistics operations
---------------------

.. autoprogram-cliff:: openstack.dcs.v1
   :command: dcs stat *
