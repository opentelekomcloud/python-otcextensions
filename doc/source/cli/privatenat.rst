Private Network Address Translation (Private NAT)
=================================================

The Private NAT client is the command-line interface (CLI) for
the Private NAT API.

For help on a specific `privatenat` command, enter:

.. code-block:: console

   $ openstack privatenat help SUBCOMMAND

.. _private_gateway:

Private NAT Gateway Operations
------------------------------

.. autoprogram-cliff:: openstack.privatenat.v3
   :command: privatenat gateway *

.. _private_snat:

Private SNAT Rule Operations
----------------------------

.. autoprogram-cliff:: openstack.privatenat.v3
   :command: privatenat snat rule *

Private Transit IP Address Operations
-------------------------------------

.. autoprogram-cliff:: openstack.privatenat.v3
   :command: privatenat transit ip *
