=================================================
Anti DDoS Service (Anti_DDoS) command-line client
=================================================

The Anti_DDoS client is the command-line interface (CLI) for
the Anti DDoS Service (Anti_DDoS) API and its extensions.

For help on a specific `antiddos` command, enter:

.. code-block:: console

   $ openstack antiddos help SUBCOMMAND

.. antiddos_floatip:

Floating IP operations
----------------------

.. autoprogram-cliff:: openstack.anti_ddos.v1
   :command: antiddos floatip *

.. antiddos_config:

Config operations
-----------------

.. autoprogram-cliff:: openstack.anti_ddos.v1
   :command: antiddos config *
