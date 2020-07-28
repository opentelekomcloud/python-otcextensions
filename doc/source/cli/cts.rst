Cloud Trace Service (CTS)
=========================

The CTS client is the command-line interface (CLI) for
the Cloud Trace Service (CTS) API and its extensions.

For help on a specific `cts` command, enter:

.. code-block:: console

   $ openstack cts help SUBCOMMAND

.. cts_traces:

Traces operations
-----------------

.. autoprogram-cliff:: openstack.cts.v1
   :command: cts trace *

.. _cts_tracker:

Tracker operations
------------------

.. autoprogram-cliff:: openstack.cts.v1
   :command: cts tracker *
