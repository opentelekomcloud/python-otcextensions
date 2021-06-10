Simple Message Notification Service (SMN)
=========================================

The SMN client is the command-line interface (CLI) for
the Simple Message Notification Service (SMN) API and its extensions.

For help on a specific `smn` command, enter:

.. code-block:: console

   $ openstack smn help SUBCOMMAND

.. _smn_topic:

Topic operations
----------------

.. autoprogram-cliff:: openstack.smn.v2
   :command: smn topic *

.. _smn_subscription:

Subscription operations
-----------------------

.. autoprogram-cliff:: openstack.smn.v2
   :command: smn subscription *

.. _smn_template:

Template operations
-------------------

.. autoprogram-cliff:: openstack.smn.v2
   :command: smn template *

.. _smn_sms:

SMS operations
--------------

.. autoprogram-cliff:: openstack.smn.v2
   :command: smn sms *

.. _smn_message:

Message operations
------------------

.. autoprogram-cliff:: openstack.smn.v2
   :command: smn message *
