OpenStack Client (CLI)
======================

The OpenStack Client is a self-contained OpenStack project providing a
command line interface to the most important cloud functions. For most
of the API calls an equivalent CLI command is available under a shared
command invoked as ``openstack``. An example is ``openstack server
list``. For reference see the documentation of the OpenStack Client
(OSC).

The OTC Extensions don't re-implement the CLI tool, but augment it
automatically. If you have installed OTC Extensions and OpenStack
Client, the latter understands many extra commands:

.. code-block:: bash

   openstack --help | grep -c otcextensions
   164

For details of the available commands, check the detailed CLI
documentation of these services:

.. toctree::
   :maxdepth: 1

   anti_ddos
   auto_scaling
   cce_v2
   cts
   dcs
   deh
   dms
   dns
   kms
   load_balancer
   obs
   rds
   volume_backup
