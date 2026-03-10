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
import json
import uuid

import openstack
from otcextensions.tests.functional import base

_logger = openstack._log.setup_logging("openstack")


def _get_access_policy():
    return json.dumps(
        {
            "Version": "2016-09-07",
            "Id": "__default_policy_ID",
            "Statement": [
                {
                    "Sid": "__user_pub_0",
                    "Effect": "Allow",
                    "Principal": {"CSP": ["*"]},
                    "Action": ["SMN:Publish", "SMN:QueryTopicDetail"],
                    "Resource": "*",
                }
            ],
        }
    )


class TestTopicAttribute(base.BaseFunctionalTest):

    uuid_v4 = uuid.uuid4().hex[:8]
    topic_name = "sdk-test-smn-attr-{uuid}".format(uuid=uuid_v4)
    topic = None

    def setUp(self):
        super(TestTopicAttribute, self).setUp()
        self.client = self.conn.smn

    def tearDown(self):
        if self.topic:
            try:
                self.client.delete_topic(self.topic)
            except openstack.exceptions.SDKException as e:
                _logger.warning(
                    "Got exception during clearing resources %s" % e.message
                )
        super(TestTopicAttribute, self).tearDown()

    def _create_topic(self):
        try:
            self.topic = self.client.create_topic(
                name=self.topic_name,
                display_name="SDK Test Topic Attribute",
            )
        except openstack.exceptions.BadRequestException:
            self.topic = self.client.find_topic(self.topic_name)

    def _set_access_policy(self):
        self.client.update_topic_attribute(
            self.topic,
            name="access_policy",
            attr_value=_get_access_policy(),
        )

    def test_01_update_topic_attribute(self):
        self._create_topic()
        result = self.client.update_topic_attribute(
            self.topic,
            name="access_policy",
            attr_value=_get_access_policy(),
        )
        self.assertIsNotNone(result.request_id)

    def test_02_list_topic_attributes(self):
        self._create_topic()
        self._set_access_policy()
        attrs = list(self.client.topic_attributes(self.topic))
        self.assertGreaterEqual(len(attrs), 1)

    def test_03_delete_topic_attribute_by_name(self):
        self._create_topic()
        self._set_access_policy()
        self.client.delete_topic_attribute(
            self.topic,
            name="access_policy",
        )
        attrs = list(self.client.topic_attributes(self.topic))
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0].attributes.access_policy, "")

    def test_04_delete_all_topic_attributes(self):
        self._create_topic()
        self._set_access_policy()
        self.client.delete_topic_attribute(self.topic)
        attrs = list(self.client.topic_attributes(self.topic))
        self.assertEqual(len(attrs), 1)
        self.assertEqual(attrs[0].attributes.access_policy, "")
