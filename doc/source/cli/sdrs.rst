Storage Disaster Recovery Service (SDRS)
========================================

The SDRS client is the command-line interface (CLI) for
the Storage Disaster Recovery Service (SDRS) API and its extensions.

For help on a specific `sdrs` command, enter:

.. code-block:: console

   $ openstack sdrs help SUBCOMMAND

.. _sdrs_active_domain:

Active-active domains operations
--------------------------------

.. autoprogram-cliff:: openstack.sdrs.v1
   :command: sdrs active domain *

.. _sdrs_job:

Job operations
--------------

.. autoprogram-cliff:: openstack.sdrs.v1
   :command: sdrs job *
