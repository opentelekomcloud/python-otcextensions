========================================
LoadBalancer service command-line client
========================================

The load_balancer client is the command-line interface (CLI) for
the native Neutron/Octavia LoadBalancer service (load_balancer) API.

For help on a specific `loadbalancer` command, enter:

.. code-block:: console

   $ openstack loadbalancer help SUBCOMMAND

.. _load_balancer:

Load Balancer operations
------------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: loadbalancer list

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: loadbalancer show

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: loadbalancer create

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: loadbalancer set

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: loadbalancer delete

.. _listener:

Listeners operations
--------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: loadbalancer listener *

.. _pool:

Pools operations
----------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer pool list

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer pool show

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer pool create

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer pool set

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer pool delete

.. _pool_member:

Pool Members operations
-----------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer member *

.. _hm:

Health Monitor operations
-------------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: loadbalancer healthmonitor *
