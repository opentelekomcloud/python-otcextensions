Network Address Translation (NAT)
=================================

The NAT client is the command-line interface (CLI) for
the Network Address Translation (NAT) API and its extensions.

For help on a specific `nat` command, enter:

.. code-block:: console

   $ openstack nat help SUBCOMMAND

.. _gateway:

Nat Gateway Operations
----------------------

.. autoprogram-cliff:: openstack.nat.v2
   :command: nat gateway *

.. _snat:

Snat Rule Operations
--------------------

.. autoprogram-cliff:: openstack.nat.v2
   :command: nat snat rule *

.. _dnat:

Dnat Rule Operations
--------------------

.. autoprogram-cliff:: openstack.nat.v2
   :command: nat dnat rule *
