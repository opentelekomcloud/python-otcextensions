Auto-Scaling (AS)
=================

.. contents:: Table of Contents
   :local:

Auto-Scaling Configuration
--------------------------

An Auto-Scaling (AS) configuration is a template of Elastic Cloud Servers in
an AS group. It defines the specifications of the instances to be added to
the AS group. The AS configuration is decoupled from the AS group and can
be used several times in different groups. Up to 100 AS configurations can
be created for each user.

List Auto-Scaling configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Auto-Scaling configurations and to filter
the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_configs.py
   :lines: 13-19

Create Auto-Scaling configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create an Auto-Scaling Configuration instance with parameters.

.. literalinclude:: ../examples/auto_scaling/create_config.py
   :lines: 16-36

Find Auto-Scaling configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to find an Auto-Scaling Configuration instance by name or id.

.. literalinclude:: ../examples/auto_scaling/find_config.py
   :lines: 16-24

Auto-Scaling Group
------------------

An Auto-Scaling (AS) group consists of a collection of instances that apply
to the same scaling scenario. An AS group specifies parameters, such as the
maximum number of instances, expected number of instances, minimum number
of instances, VPC, subnet, and load balancing. Each user can create a maximum
of 25 AS groups by default.
