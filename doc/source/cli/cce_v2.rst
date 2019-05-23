================================================
Cloud Container Engine (CCE) command-line client
================================================

The CCE client is the command-line interface (CLI) for
the Cloud Container Engine (CCE) API and its extensions for the CCE v2.
It can be enabled by either adding `cce_api_version: 3` into the clouds.yaml
or `OS_CCE_API_VERSION=3` environment variable or flag to the OSC.

For help on a specific `cce` command, enter:

.. code-block:: console

   $ openstack cce help SUBCOMMAND

.. _cluster:

Cluster v2 operations
---------------------

.. autoprogram-cliff:: openstack.cce.v3
   :command: cce cluster *
