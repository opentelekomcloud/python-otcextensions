========================================
LoadBalancer service command-line client
========================================

The load_balancer client is the command-line interface (CLI) for
the native Neutron/Octavia LoadBalancer service (load_balancer) API.

For help on a specific `load balancer` command, enter:

.. code-block:: console

   $ openstack load balancer help SUBCOMMAND

.. _load_balancer:

Load Balancer operations
------------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: load balancer list

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: load balancer show

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: load balancer create

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: load balancer update

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: load balancer delete

.. _listener:

Listeners operations
--------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
   :command: load balancer listener *

.. _pool:

Pools operations
----------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer pool list

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer pool show

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer pool create

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer pool update

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer pool delete

.. _pool_member:

Pool Members operations
-----------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer pool member *

.. _hm:

Health Monitor operations
-------------------------

.. autoprogram-cliff:: openstack.load_balancer.v1
  :command: load balancer health monitor *
