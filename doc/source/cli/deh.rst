================================================
Dedicated Host Service (DeH) command-line client
================================================

The DeH client is the command-line interface (CLI) for
the Dedicated Host Service (DeH) API and its extensions.

For help on a specific `deh` command, enter:

.. code-block:: console

   $ openstack deh help SUBCOMMAND

.. _deh_host:

Host operations
---------------

.. autoprogram-cliff:: openstack.deh.v1
   :command: deh host *

.. _deh_server:

Server operations
-----------------

.. autoprogram-cliff:: openstack.deh.v1
   :command: deh server *
