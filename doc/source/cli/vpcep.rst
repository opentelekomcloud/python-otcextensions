VPC Endpoint Service (VPCEP)
============================

The VPCEP client is the command-line interface (CLI) for
the VPC Endpoint Service (VPCEP) API and its extensions.

For help on a specific `vpcep` command, enter:

.. code-block:: console

   $ openstack vpcep help SUBCOMMAND

.. _vpcep_endpoint:

Vpcep Endpoint Operations
-------------------------

.. autoprogram-cliff:: openstack.vpcep.v1
   :command: vpcep endpoint *

.. _vpcep_service:

Vpcep Service Operations
------------------------

.. autoprogram-cliff:: openstack.vpcep.v1
   :command: vpcep service *

.. _vpcep_quota:

Vpcep Quota Operations
----------------------

.. autoprogram-cliff:: openstack.vpcep.v1
   :command: vpcep quota *
