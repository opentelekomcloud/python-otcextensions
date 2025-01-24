Cloud Search Service (CSS)
==========================

The CSS client is the command-line interface (CLI) for
the Cloud Search Service (CSS) API and its extensions.

For help on a specific `css` command, enter:

.. code-block:: console

   $ openstack css help SUBCOMMAND

.. _css_cluster:

CSS Cluster Operations
----------------------

.. autoprogram-cliff:: openstack.css.v1
   :command: css cluster *

.. _snapshot:

CSS Snapshot Operations
-----------------------

.. autoprogram-cliff:: openstack.css.v1
   :command: css snapshot *

CSS SSL Certificate
-------------------

.. autoprogram-cliff:: openstack.css.v1
   :command: css certificate *
