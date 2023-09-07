Data Ingestion Service (DIS)
============================

The DIS client is the command-line interface (CLI) for
the Data Ingestion Service (DIS) API and its extensions.

For help on a specific `dis` command, enter:

.. code-block:: console

   $ openstack dis help SUBCOMMAND

.. _app:

DIS App Operations
------------------

.. autoprogram-cliff:: openstack.dis.v2
   :command: dis app *

.. _checkpoint:

DIS Checkpoint Operations
-------------------------

.. autoprogram-cliff:: openstack.dis.v2
   :command: dis checkpoint *

.. _data:

DIS Data Operations
-------------------

.. autoprogram-cliff:: openstack.dis.v2
   :command: dis data *

.. _dump_task:

DIS Dump Task Operations
------------------------

.. autoprogram-cliff:: openstack.dis.v2
   :command: dis dump task *

.. _stream:

DIS Stream Operations
---------------------

.. autoprogram-cliff:: openstack.dis.v2
   :command: dis stream *
