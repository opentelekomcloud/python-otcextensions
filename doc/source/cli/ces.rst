Cloud Eye Service (CES)
=======================

The CES client is the command-line interface (CLI) for
the Cloud Eye Service (CES) API and its extensions.

For help on a specific `ces` command, enter:

.. code-block:: console

   $ openstack ces help SUBCOMMAND

.. _alarm:

Alarm Rule Operations
---------------------

.. autoprogram-cliff:: openstack.ces.v1
   :command: ces alarm *

.. _metric:

Metric Operations
-----------------

.. autoprogram-cliff:: openstack.ces.v1
   :command: ces metric *

.. _quota:

Quota Operations
----------------

.. autoprogram-cliff:: openstack.ces.v1
   :command: ces quota *

.. _event_data:

Event Data Operations
---------------------

.. autoprogram-cliff:: openstack.ces.v1
   :command: ces event data *
