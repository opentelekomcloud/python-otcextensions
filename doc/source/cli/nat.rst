=====================================================
Network Address Translation (nat) command-line client
=====================================================

The NAT client is the command-line interface (CLI) for
the Database service (NAT) API and its extensions.

For help on a specific `nat` command, enter:

.. code-block:: console

   $ openstack nat help SUBCOMMAND

.. _gateway:

NAT Gateway operations
----------------------

.. autoprogram-cliff:: openstack.nat.v2
   :command: nat gateway *

.. _snat:

SNAT Rule operations
--------------------

.. autoprogram-cliff:: openstack.nat.v2
   :command: nat snat *

.. _dnat:

DNAT Rule operations
--------------------

.. autoprogram-cliff:: openstack.nat.v2
   :command: nat dnat *
