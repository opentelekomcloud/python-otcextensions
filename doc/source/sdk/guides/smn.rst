Simple Message Notification Service (SMN)
=========================================

The Simple Message Notification service in the Open Telekom Cloud offers
three APIs for creating topics (a combination of a message and a logical
access point), adding message subscribers and sending out messages. The
SMN services includes the two roles publisher and subscriber. In
contrast to the Distributed Message Service, a subscriber can also be
external: an email address, a telephone number, a message queue or a URL.
SMN is easy to integrate with other services and can thus act as an
intermediary for data exchange. The service works with redundant message
nodes – if one of the nodes fails, another one is used instead. This ensures
that the messages are transmitted reliably, regardless of how they are sent.
SMN delivers the messages to various end points in a readable format (SMS,
email, http/s).

.. contents:: Table of Contents
   :local:

Topic
-----

A topic is a specified event to publish messages and subscribe to
notifications. It serves as a message sending channel, where publishers
and subscribers can interact with each other.

List Topics
^^^^^^^^^^^

This interface is used to query SMN Topics and to filter
the output with query parameters.

.. literalinclude:: ../examples/smn/list_topics.py
   :lines: 16-23

Get Topic
^^^^^^^^^

This interface is used to get a SMN topic by ID or an instance of
class :class:`~otcextensions.sdk.smn.v2.topic.Topic`.

.. literalinclude:: ../examples/smn/get_topic.py
   :lines: 16-24

Create Topic
^^^^^^^^^^^^

This interface is used to create a SMN topic instance with
parameters.

.. literalinclude:: ../examples/smn/create_topic.py
   :lines: 16-27

Update Topic
^^^^^^^^^^^^

This interface is used to update a SMN topic instance with
parameters.

.. literalinclude:: ../examples/smn/update_topic.py
   :lines: 16-29

Delete Topic
^^^^^^^^^^^^

This interface is used to delete a SMN topic instance by id
or an instance of class
:class:`~otcextensions.sdk.smn.v2.topic.Topic`.

.. literalinclude:: ../examples/smn/delete_topic.py
   :lines: 16-24

List Topics Attributes
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to query SMN topic attributes and to filter
the output with query parameters.

.. literalinclude:: ../examples/smn/list_topic_attributes.py
   :lines: 16-27

Update Topic Attribute
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to update a SMN topic attribute instance with
parameters.

.. literalinclude:: ../examples/smn/update_topic_attribute.py
   :lines: 16-27

Delete Topic Attribute
^^^^^^^^^^^^^^^^^^^^^^

This interface is used to delete a SMN topic attribute.

.. literalinclude:: ../examples/smn/delete_topic_attribute.py
   :lines: 16-27

Subscription
------------

To deliver messages published to a topic to endpoints, you must
add the subscription endpoints to the topic. Endpoints can be email
addresses, phone numbers, message queues, and HTTP/HTTPS URLs. After you add
endpoints to the topic and the subscribers confirm the subscription, they
are able to receive messages published to the topic.
You can add multiple subscriptions to each topic. This section describes
how to add subscriptions to a topic you created or one to which you have
been granted permissions and how to delete subscriptions.

List Subscriptions
^^^^^^^^^^^^^^^^^^

This interface is used to query SMN Subscription and to filter
the output with query parameters.

.. literalinclude:: ../examples/smn/list_subscriptions.py
   :lines: 16-27

Create Subscription
^^^^^^^^^^^^^^^^^^^

This interface is used to create a subscription instance to a SMN topic.

.. literalinclude:: ../examples/smn/create_subscription.py
   :lines: 16-30

Delete Subscription
^^^^^^^^^^^^^^^^^^^

This interface is used to delete a SMN subscription instance by id
or an instance of class
:class:`~otcextensions.sdk.smn.v2.subscription.Subscription`.

.. literalinclude:: ../examples/smn/delete_subscription.py
   :lines: 16-23


Template
--------

Message templates contain fixed and changeable content and can be used
to send messages quickly. When you publish a message using a template,
you can specify values for variables in the template.
Message templates are grouped by template name. You can create templates
for different protocols using the same template name. You must specify the
default protocol in any template name, or the system will not allow you to
publish messages using that template name. When sending messages using a
template, SMN tries to match different types of subscribers to the template
protocols. If there is no template for a specified protocol, SMN will use
the default template to send messages to subscribers of that protocol.

List Template
^^^^^^^^^^^^^

This interface is used to query SMN message templates and to filter
the output with query parameters.

.. literalinclude:: ../examples/smn/list_templates.py
   :lines: 16-23

Get Template
^^^^^^^^^^^^

This interface is used to get a SMN message template by ID or an instance of
class :class:`~otcextensions.sdk.smn.v2.template.Template`.

.. literalinclude:: ../examples/smn/get_template.py
   :lines: 16-24

Find Template
^^^^^^^^^^^^^

This interface is used to find a SMN message template by name or ID.

.. literalinclude:: ../examples/smn/find_template.py
   :lines: 16-24


Create Template
^^^^^^^^^^^^^^^

This interface is used to create a SMN template instance with
parameters.

.. literalinclude:: ../examples/smn/create_template.py
   :lines: 16-28

Update Template
^^^^^^^^^^^^^^^

This interface is used to update a SMN message template instance with
parameters.

.. literalinclude:: ../examples/smn/update_template.py
   :lines: 16-28

Delete Template
^^^^^^^^^^^^^^^

This interface is used to delete a SMN message template instance by id
or an instance of class
:class:`~otcextensions.sdk.smn.v2.template.Template`.

.. literalinclude:: ../examples/smn/delete_template.py
   :lines: 16-24

Message Publishing
------------------

Use the message structure to publish a message to the topic. After the
message ID is returned, the message has been saved and is to be pushed
to the subscribers of the topic. This API allows you to send different
message content to different types of subscribers.

.. literalinclude:: ../examples/smn/publish_message.py
   :lines: 16-31

SMS Publishing
--------------

Send a transactional SMS message to a specified phone number, usually used
for verification code or notification.

.. literalinclude:: ../examples/smn/send_sms.py
   :lines: 16-27

