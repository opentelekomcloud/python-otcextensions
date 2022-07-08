Direct Connect (DCAAS)
======================

The DCAAS client is the command-line interface (CLI) for
the Network Direct Connection (DCAAS) API and its extensions.

For help on a specific `dcaas` command, enter:

.. code-block:: console

   $ openstack dcaas help SUBCOMMAND

.. _connection:

Direct Connect Operations
-------------------------

.. autoprogram-cliff:: openstack.dcaas.v2
   :command: dcaas connection *

.. _endpoint_group:

Direct Connect Endpoint Group Operations
----------------------------------------

.. autoprogram-cliff:: openstack.dcaas.v2
   :command: dcaas endpoint group *

.. _virtual_gateway:

Virtual Gateway Operations
--------------------------

.. autoprogram-cliff:: openstack.dcaas.v2
   :command: dcaas gateway *
