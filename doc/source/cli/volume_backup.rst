===============================================
Volume Backup Service (VBS) command-line client
===============================================

The VBS client is the command-line interface (CLI) for
the Volume Backup service (vbs) API and its extensions.

For help on a specific `vbs` command, enter:

.. code-block:: console

   $ openstack vbs help SUBCOMMAND

.. _policy:

VBS Backup operations
---------------------

Volume backup openrations are supported through native openstackclient

.. autoprogram-cliff:: openstack.volume.v2
   :command: volume backup *


VBS Policy operations
---------------------

.. autoprogram-cliff:: openstack.volume_backup.v2
   :command: vbs policy *
