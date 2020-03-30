Object Storage service (obs)
============================

The OBS client is the command-line interface (CLI) for
the ObjectBlockStorage service (OBS) API and its extensions.

For help on a specific `obs` command, enter:

.. code-block:: console

   $ openstack obs help SUBCOMMAND

.. _container:

Container (bucket) operations
-----------------------------

.. autoprogram-cliff:: openstack.obs.v1
  :command: obs container *

.. _object:

Object operations
-----------------

.. autoprogram-cliff:: openstack.obs.v1
   :command: obs object *
