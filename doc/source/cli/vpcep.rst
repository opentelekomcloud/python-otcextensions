VPC Endpoint Service (VPCEP)
============================

The VPCEP client is the command-line interface (CLI) for
the VPC Endpoint Service (VPCEP) API and its extensions.

For help on a specific `vpcep` command, enter:

.. code-block:: console

   $ openstack vpcep help SUBCOMMAND

.. _endpoint:

Vpcep Endpoint Operations
-------------------------

.. autoprogram-cliff:: openstack.vpcep.v1
   :command: vpcep endpoint *

.. _service:

Vpcep Service Operations
------------------------

.. autoprogram-cliff:: openstack.vpcep.v1
   :command: vpcep service *

.. _quota:

Vpcep Quota Operations
----------------------

.. autoprogram-cliff:: openstack.vpcep.v1
   :command: vpcep quota *
