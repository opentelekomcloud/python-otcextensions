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

List Auto-Scaling Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Auto-Scaling configurations and to filter
the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_configs.py
   :lines: 16-22

Create Auto-Scaling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to create an Auto-Scaling Configuration instance with
parameters.

.. literalinclude:: ../examples/auto_scaling/create_config.py
   :lines: 16-36

Get Auto-Scaling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to get an Auto-Scaling Configuration by ID
or an instance of :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`.

.. literalinclude:: ../examples/auto_scaling/get_config.py
   :lines: 16-24

Find Auto-Scaling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to find an Auto-Scaling Configuration instance by
name or id.

.. literalinclude:: ../examples/auto_scaling/find_config.py
   :lines: 16-24

Delete Auto-Scaling Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete an Auto-Scaling Configuration instance by id
or an instance of :class:`~otcextensions.sdk.auto_scaling.v1.config.Config`.

.. literalinclude:: ../examples/auto_scaling/delete_config.py
   :lines: 16-23

Batch Delete Auto-Scaling Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete multiple Auto-Scaling Configuration instances
by id or an instance of
:class:`~otcextensions.sdk.auto_scaling.v1.config.Config`.

.. literalinclude:: ../examples/auto_scaling/batch_delete_config.py
   :lines: 16-26


Auto-Scaling Group
------------------

An Auto-Scaling (AS) group consists of a collection of instances that apply
to the same scaling scenario. An AS group specifies parameters, such as the
maximum number of instances, expected number of instances, minimum number
of instances, VPC, subnet, and load balancing. Each user can create a maximum
of 25 AS groups by default.

List Auto-Scaling Groups
^^^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query all Auto-Scaling Groups and to filter
the output with query parameters.

.. literalinclude:: ../examples/auto_scaling/list_groups.py
   :lines: 16-22
