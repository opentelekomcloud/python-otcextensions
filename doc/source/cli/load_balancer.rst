==============================================
LoadBalancer service (ULB) command-line client
==============================================

The ULB client is the command-line interface (CLI) for
the native Neutron/Octavia LoadBalancer service (load_balancer) API.

For help on a specific `ulb` command, enter:

.. code-block:: console

   $ openstack ulb help SUBCOMMAND

.. _load_balancer:

Load Balancer operations
------------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: ulb list

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: ulb show

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: ulb create

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: ulb update

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: ulb delete

.. _listener:

Listeners operations
--------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: ulb listener *

.. _pool:

Pools operations
----------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb pool list

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb pool show

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb pool create

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb pool update

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb pool delete

.. _pool_member:

Pool Members operations
-----------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb pool member *

.. _hm:

Health Monitor operations
-------------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: ulb health monitor *
