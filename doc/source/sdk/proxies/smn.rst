SMN API
=======

.. automodule:: otcextensions.sdk.smn.v2._proxy

The Simple Message Notification Service Class
---------------------------------------------

The SMN high-level interface is available through the ``smn``
member of a :class:`~openstack.connection.Connection` object.  The
``smn`` member will only be added if the
``otcextensions.sdk.register_otc_extensions(conn)`` method is called.

Subscription Operations
^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.smn.v2._proxy.Proxy
  :noindex:
  :members: subscriptions, create_subscription, delete_subscription

SMS Operations
^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.smn.v2._proxy.Proxy
  :noindex:
  :members: send_sms

Template Operations
^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.smn.v2._proxy.Proxy
  :noindex:
  :members: templates, get_template, find_template, create_template,
            update_template, delete_template

Topic Operations
^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.smn.v2._proxy.Proxy
  :noindex:
  :members: topics, get_topic, create_topic, delete_topic, update_topic


Topic Attribute Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.smn.v2._proxy.Proxy
  :noindex:
  :members: topic_attributes, update_topic_attribute, delete_topic_attribute

Message Operations
^^^^^^^^^^^^^^^^^^

.. autoclass:: otcextensions.sdk.smn.v2._proxy.Proxy
  :noindex:
  :members: publish_message
