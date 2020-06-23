# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from otcextensions.sdk.smn.v2 import topic as _topic
from otcextensions.sdk.smn.v2 import subscription as _subscription
from otcextensions.sdk.smn.v2 import template as _template
from otcextensions.sdk.smn.v2 import message as _message

from openstack import proxy


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Topic ========
    def create_topic(self, **attrs):
        """Create a new topic from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.smn.v2.topic.Topic`

        :returns: :class:`~otcextensions.sdk.smn.v2.topic.Topic`
        """
        return self._create(_topic.Topic, **attrs)

    def delete_topic(self, topic, ignore_missing=True):
        """Delete a topic

        :param topic: topic urn or an instance of
            :class:`~otcextensions.sdk.smn.v2.topic.Topic`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the topic does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent topic.

        :returns: ``None``
        """
        return self._delete(_topic.Topic, topic,
                            ignore_missing=ignore_missing)

    def topics(self, **query):
        """Return a generator of SMN topics

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of topic objects

        :rtype: :class:`~otcextensions.sdk.smn.v2.topic.Topic`
        """
        return self._list(_topic.Topic, **query)

    def get_topic(self, topic):
        """Get details a SMN topic

        :param topic: The value can be the ID of a topic or a
                        :class:`~otcextensions.sdk.smn.v2.topic.Topic`
                        instance.

        :returns: One :class:`~otcextensions.sdk.smn.v2.topic.Topic`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
                 when no resource can be found.
        """
        return self._get(_topic.Topic, topic)

    def update_topic(self, topic, **attrs):
        """Update a SMN topic

        :param topic: Either the ID of a topic or a
                       :class:`~otcextensions.sdk.smn.v2.topic.Topic`
                       instance.
        :param dict attrs: The attributes to update on the topic represented
                       by :class:`~otcextensions.sdk.smn.v2.topic.Topic`

        :returns: The updated topic.

        :rtype: :class:`~otcextensions.sdk.smn.v2.topic.Topic`
        """
        return self._update(_topic.Topic, topic, **attrs)

    def find_topic(self, name_or_id, ignore_missing=False):
        """Find a single SMN topic

        :param name_or_id: The name or ID of a topic.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the topic does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent topic.

        :returns: One :class:`~otcextensions.sdk.smn.v2.topic.Topic`
        """
        return self._find(_topic.Topic, name_or_id,
                          ignore_missing=ignore_missing)

    # ======== Subscription ========

    def create_subscription(self, topic, **attrs):
        """Create a new Subscription from attributes

        :param topic: Either the ID of a topic or a
            :class:`~otcextensions.sdk.smn.v2.topic.Topic`
            instance.
        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.smn.v2.subscription.Subscription`

        :returns: :class:`~otcextensions.sdk.smn.v2.subscription.Subscription`
        """
        topic_urn = self._find(_topic.Topic, topic).topic_urn
        base_path = '/notifications/topics/' + topic_urn + '/subscriptions'
        return self._create(_subscription.Subscription,
                            base_path=base_path, **attrs)

    def delete_subscription(self, subscription, ignore_missing=True):
        """Delete a subscription

        :param subscription: Either the ID of a subscription or a
            :class: `~otcextensions.sdk.smn.v2.subscription.Subscription`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            if the subscription does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent subscription.

        :returns: ``None``
        """
        return self._delete(_subscription.Subscription, subscription,
                            ignore_missing=ignore_missing)

    def subscriptions(self, topic=None, **query):
        """Return a generator of Subscriptions

        :param topic: Either the ID of a subscription or a
            :class: `~otcextensions.sdk.smn.v2.subscription.Subscription`
            instance.
        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of subscription objects

        :rtype: :class:`~otcextensions.sdk.smn.v2.subscription.Subscription`
        """
        if topic:
            topic_urn = self._find(_topic.Topic, topic).topic_urn
            base_path = '/notifications/topics/' + topic_urn + '/subscriptions'
            return self._list(_subscription.Subscription,
                              base_path=base_path, **query)
        return self._list(_subscription.Subscription, **query)

    # ======== Template ========
    def create_template(self, **attrs):
        """Create a new message template from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.smn.v2.template.Template`

        :returns: :class:`~otcextensions.sdk.smn.v2.template.Template
        """
        return self._create(_template.Template, **attrs)

    def delete_template(self, template, ignore_missing=True):
        """Delete a message template

        :param template: message template ID or an instance of
            :class:`~otcextensions.sdk.smn.v2.template.Template`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the template does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent template.

        :returns: ``None``
        """
        return self._delete(_template.Template, template,
                            ignore_missing=ignore_missing)

    def templates(self, **query):
        """Return a generator of message templates

        :param dict query: Optional query parameters to be sent to limit
            the resources being returned.

        :returns: A generator of template objects.

        :rtype: :class:`~otcextensions.sdk.smn.v2.template.Template`
        """
        return self._list(_template.Template, **query)

    def get_template(self, template):
        """Get details a message templates

        :param template: The value can be the ID of a message template or a
            :class:`~otcextensions.sdk.smn.v2.template.Template `instance.

        :returns: One :class:`~otcextensions.sdk.smn.v2.template.Template`

        :raises: :class:`~openstack.exceptions.ResourceNotFound`
            when no resource can be found.
        """
        return self._get(_template.Template, template)

    def update_template(self, template, **attrs):
        """Update a message template

        :param topic: Either the ID of a message template or a
            :class:`~otcextensions.sdk.smn.v2.template.Template` instance.
        :param dict attrs: The attributes to update on the template represented
            by :class:`~otcextensions.sdk.smn.v2.template.Template`

        :returns: The updated template.

        :rtype: :class:`~otcextensions.sdk.smn.v2.template.Template`
        """
        return self._update(_topic.Template, template, **attrs)

    def find_template(self, name_or_id, ignore_missing=False):
        """Find a single message template.

        :param name_or_id: The name or ID of a template.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the template does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent template.

        :returns: One :class:`~otcextensions.sdk.smn.v2.template.Template`
        """
        return self._find(_template.Template, name_or_id,
                          ignore_missing=ignore_missing)


    # ======== Message Publish ========
    def publish_message(self, topic, **attrs):
        """Publish messages in the text format or
            using message structure or using a message template
            to a topic.

        :param dict attrs: Keyword arguments which will be used to Publish
            a Message.

        :returns: :class:`~otcextensions.sdk.smn.v2.message.Message
        """
        topic = self._find(_topic.Topic, topic, ignore_missing=False)
        return self._create(_message.Message, topic_urn=topic.urn, **attrs)
