=============================================
Domain Name Service (DNS) command-line client
=============================================

The DNS client is the command-line interface (CLI) for
the Domain Name Service (DNS) API and its extensions.

For help on a specific `dns` command, enter:

.. code-block:: console

   $ openstack dns help SUBCOMMAND

.. _dns_zone:

Zone operations
---------------

.. autoprogram-cliff:: openstack.dns.v2
   :command: dns zone *

.. _dns_rs:

Recordset operations
--------------------

.. autoprogram-cliff:: openstack.dns.v2
   :command: dns recordset *

.. _dns_ptr:

PTR operations
--------------

.. autoprogram-cliff:: openstack.dns.v2
   :command: dns ptr *
