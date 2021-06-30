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

from otcextensions.sdk.smn.v2 import _proxy
from otcextensions.sdk.smn.v2 import topic
from otcextensions.sdk.smn.v2 import template
from otcextensions.sdk.smn.v2 import subscription
from otcextensions.sdk.smn.v2 import message
from otcextensions.sdk.smn.v2 import sms

from openstack.tests.unit import test_proxy_base


class TestSmnProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestSmnProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSmnTopic(TestSmnProxy):
    def test_topic_create(self):
        self.verify_create(self.proxy.create_topic, topic.Topic,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_topic_delete(self):
        self.verify_delete(self.proxy.delete_topic,
                           topic.Topic, True)

    def test_topic_get(self):
        self.verify_get(self.proxy.get_topic, topic.Topic)

    def test_topics(self):
        self.verify_list(self.proxy.topics, topic.Topic)

    def test_topic_update(self):
        self.verify_update(self.proxy.update_topic, topic.Topic)


class TestSmnTemplate(TestSmnProxy):
    def test_template_create(self):
        self.verify_create(self.proxy.create_template, template.Template,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_template_delete(self):
        self.verify_delete(self.proxy.delete_template,
                           template.Template, True)

    def test_template_get(self):
        self.verify_get(self.proxy.get_template, template.Template)

    def test_templates(self):
        self.verify_list(self.proxy.templates, template.Template)

    def test_template_update(self):
        self.verify_update(self.proxy.update_template, template.Template)


class TestSmnSubscription(TestSmnProxy):
    def test_subscription_create(self):
        self.verify_create(
            self.proxy.create_subscription, subscription.Subscription,
            method_args=['topic_id'],
            method_kwargs={'name': 'id'},
            expected_kwargs={'topic_urn': 'topic_id', 'name': 'id'}
        )

    def test_subscription_delete(self):
        self.verify_delete(self.proxy.delete_subscription,
                           subscription.Subscription, True)

    def test_subscriptions(self):
        self.verify_list(self.proxy.subscriptions, subscription.Subscription)

    def test_topic_subscriptions(self):
        self.verify_list(
            self.proxy.subscriptions, subscription.Subscription,
            method_args=['topic_id'],
            expected_kwargs={'topic_urn': 'topic_id'}
        )


class TestSmnMessage(TestSmnProxy):
    def test_publish_message(self):
        self.verify_create(
            self.proxy.publish_message, message.Message,
            method_args=['topic_id'],
            method_kwargs={'subject': 'Test Message'},
            expected_kwargs={
                'topic_urn': 'topic_id',
                'subject': 'Test Message'}
        )


class TestSmnSms(TestSmnProxy):
    def test_send_sms(self):
        self.verify_create(
            self.proxy.send_sms, sms.Sms,
            method_kwargs={
                'endpoint': '+999999',
                'message': 'Test SMS'
            },
            expected_kwargs={
                'endpoint': '+999999',
                'message': 'Test SMS'
            }
        )
