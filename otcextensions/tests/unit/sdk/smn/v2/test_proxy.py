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

from openstack.tests.unit import test_proxy_base
from otcextensions.sdk.smn.v2 import _proxy
from otcextensions.sdk.smn.v2 import message
from otcextensions.sdk.smn.v2 import sms
from otcextensions.sdk.smn.v2 import subscription
from otcextensions.sdk.smn.v2 import template
from otcextensions.sdk.smn.v2 import topic


class TestSmnProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestSmnProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSmnTopic(TestSmnProxy):
    def test_topic_create(self):
        self.verify_create(
            self.proxy.create_topic,
            topic.Topic,
            method_kwargs={"name": "id"},
            expected_kwargs={"name": "id"},
        )

    def test_topic_delete(self):
        self.verify_delete(self.proxy.delete_topic, topic.Topic, True)

    def test_topic_get(self):
        self.verify_get(self.proxy.get_topic, topic.Topic)

    def test_topics(self):
        self.verify_list(self.proxy.topics, topic.Topic)

    def test_topic_update(self):
        self.verify_update(self.proxy.update_topic, topic.Topic)


class TestSmnTemplate(TestSmnProxy):
    def test_template_create(self):
        self.verify_create(
            self.proxy.create_template,
            template.Template,
            method_kwargs={"name": "id"},
            expected_kwargs={"name": "id"},
        )

    def test_template_delete(self):
        self.verify_delete(self.proxy.delete_template, template.Template, True)

    def test_template_get(self):
        self.verify_get(self.proxy.get_template, template.Template)

    def test_templates(self):
        self.verify_list(self.proxy.templates, template.Template)

    def test_template_update(self):
        self.verify_update(self.proxy.update_template, template.Template)


class TestSmnSubscription(TestSmnProxy):
    def test_subscription_create(self):
        self.verify_create(
            self.proxy.create_subscription,
            subscription.Subscription,
            method_args=["topic_id"],
            method_kwargs={"name": "id"},
            expected_kwargs={"topic_urn": "topic_id", "name": "id"},
            expected_args=[],
        )

    def test_subscription_delete(self):
        self.verify_delete(
            self.proxy.delete_subscription, subscription.Subscription, True
        )

    def test_subscriptions(self):
        self.verify_list(self.proxy.subscriptions, subscription.Subscription)

    def test_topic_subscriptions(self):
        self.verify_list(
            self.proxy.subscriptions,
            subscription.Subscription,
            method_args=["topic_id"],
            expected_kwargs={"topic_urn": "topic_id"},
            expected_args=[],
        )


class TestSmnMessage(TestSmnProxy):
    def test_publish_message(self):
        self.verify_create(
            self.proxy.publish_message,
            message.Message,
            method_args=["topic_id"],
            method_kwargs={"subject": "Test Message"},
            expected_kwargs={"topic_urn": "topic_id", "subject": "Test Message"},
            expected_args=[],
        )


class TestSmnSms(TestSmnProxy):
    def test_send_sms(self):
        self.verify_create(
            self.proxy.send_sms,
            sms.Sms,
            method_kwargs={"endpoint": "+999999", "message": "Test SMS"},
            expected_kwargs={"endpoint": "+999999", "message": "Test SMS"},
        )


class TestExtractName(TestSmnProxy):

    def test_extract_name(self):
        self.assertEqual(
            ["topic"],
            self.proxy._extract_name(
                "/v2/123/notifications/topics/"
                "urn:smn:regionId:8bad8a40e0f7462f8c1676e3f93a8183:"
                "test_create_topic_v2",
                project_id="123",
            ),
        )
        self.assertEqual(
            ["topics"],
            self.proxy._extract_name(
                "/v2/123/notifications/topics",
                project_id="123",
            ),
        )
        self.assertEqual(
            ["topic", "attributes"],
            self.proxy._extract_name(
                "/v2/123/notifications/topics/"
                "urn:smn:regionId:8bad8a40e0f7462f8c1676e3f93a8183:"
                "test_create_topic_v2/attributes/access_policy",
                project_id="123",
            ),
        )
        self.assertEqual(
            ["topic", "publish"],
            self.proxy._extract_name(
                "/v2/123/notifications/topics/"
                "urn:smn:regionId:8bad8a40e0f7462f8c1676e3f93a8183:"
                "test_create_topic_v2/publish",
                project_id="123",
            ),
        )
        self.assertEqual(
            ["subscription"],
            self.proxy._extract_name(
                "/v2/123/notifications/subscriptions/"
                "urn:smn:regionId:8bad8a40e0f7462f8c1676e3f93a8183:"
                "test_create_topic_v2:subscription_id",
                project_id="123",
            ),
        )
        self.assertEqual([], self.proxy._extract_name("/", project_id="123"))

    def test_extract_name_for_documented_endpoints(self):
        topic_urn = (
            "urn:smn:regionId:8bad8a40e0f7462f8c1676e3f93a8183:"
            "test_create_topic_v2"
        )
        subscription_urn = f"{topic_urn}:subscription_id"
        endpoints = [
            ("/", []),
            ("/v2", []),
            ("/v2/123/notifications/topics", ["topics"]),
            (f"/v2/123/notifications/topics/{topic_urn}", ["topic"]),
            (
                f"/v2/123/notifications/topics/{topic_urn}/attributes",
                ["topic", "attributes"],
            ),
            (
                f"/v2/123/notifications/topics/{topic_urn}/attributes/access_policy",
                ["topic", "attributes"],
            ),
            (
                f"/v2/123/notifications/topics/{topic_urn}/publish",
                ["topic", "publish"],
            ),
            (
                f"/v2/123/notifications/topics/{topic_urn}/subscriptions",
                ["topic", "subscriptions"],
            ),
            ("/v2/123/notifications/subscriptions", ["subscriptions"]),
            (
                f"/v2/123/notifications/subscriptions/{subscription_urn}",
                ["subscription"],
            ),
            ("/v2/123/notifications/message_template", ["message_template"]),
            (
                "/v2/123/notifications/message_template/"
                "57ba8dcecda844878c5dd5815b65d10f",
                ["message_template"],
            ),
            ("/v2/123/smn_topic/tags", ["smn_topic", "tags"]),
            (
                f"/v2/123/smn_topic/{topic_urn}/tags",
                ["smn_topic", "tags"],
            ),
            (
                f"/v2/123/smn_topic/{topic_urn}/tags/env.prod",
                ["smn_topic", "tags"],
            ),
            (
                f"/v2/123/smn_topic/{topic_urn}/tags/action",
                ["smn_topic", "tags", "action"],
            ),
            (
                "/v2/123/smn_topic/resource_instances/action",
                ["smn_topic", "resource_instances", "action"],
            ),
        ]

        for url, expected in endpoints:
            with self.subTest(url=url):
                self.assertEqual(
                    expected, self.proxy._extract_name(url, project_id="123")
                )
