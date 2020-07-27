Network Address Translation (NAT)
=================================

The VPC client is the command-line interface (CLI) for
the Virtual Private Cloud (VPC) API and its extensions.

For help on a specific `vpc` command, enter:

.. code-block:: console

   $ openstack vpc help SUBCOMMAND

.. _peering:

Vpc Peering Operations
----------------------

.. autoprogram-cliff:: openstack.vpc.v2
   :command: vpc peering *

.. _route:

Vpc Route Operations
--------------------

.. autoprogram-cliff:: openstack.vpc.v2
   :command: vpc route *
