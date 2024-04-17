Modelarts Service (modelarts)
=============================

The Modelarts client is the command-line interface (CLI) for
the ModelArts service API and its extensions.

For help on a specific `rds` command, enter:

.. code-block:: console

   $ openstack ma help SUBCOMMAND

.. _builtin_model:

Built-In Model Operations
-------------------------

.. autoprogram-cliff:: openstack.modelartsv1.v1
   :command: ma builtin model *

.. _devenv:

Devenv Operations
-----------------

.. autoprogram-cliff:: openstack.modelartsv1.v1
   :command: ma devenv *

.. _model:

Model Operations
----------------

.. autoprogram-cliff:: openstack.modelartsv1.v1
   :command: ma model *

.. _service:

Service Operations
------------------

.. autoprogram-cliff:: openstack.modelartsv1.v1
   :command: ma service *

.. _training_job:

Training Job Operations
-----------------------

.. autoprogram-cliff:: openstack.modelartsv1.v1
   :command: ma training job *

.. _visualization_job:

Visualization Job Operations
----------------------------

.. autoprogram-cliff:: openstack.modelartsv1.v1
   :command: ma visualization job *

.. _dataset:

Dataset Operations
------------------

.. autoprogram-cliff:: openstack.modelartsv2.v2
   :command: ma dataset *

