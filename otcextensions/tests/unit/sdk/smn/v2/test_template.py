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

from openstack.tests.unit import base

from otcextensions.sdk.smn.v2 import template


EXAMPLE = {
    "message_template_name": "confirm_message",
    "protocol": "https",
    "update_time": "2016-08-02T08:22:25Z",
    "create_time": "2016-08-02T08:22:20Z",
    "request_id": "ba79ca8f794f4f50985ce7b98a401b47",
    "tag_names": [
        "topic_id_id4"
    ],
    "content": "(1/24)You are invited to subscribe to topic({topic_id_id4}).",
    "message_template_id": "57ba8dcecda844878c5dd5815b65d10f"
}


class TestTemplate(base.TestCase):

    def test_basic(self):
        sot = template.Template()
        self.assertEqual('message_templates', sot.resources_key)
        path = '/notifications/message_template'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = template.Template(**EXAMPLE)
        self.assertEqual(EXAMPLE['message_template_name'],
                         sot.name)
        self.assertEqual(EXAMPLE['message_template_id'],
                         sot.id)
        self.assertEqual(EXAMPLE['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE['update_time'], sot.update_time)
        self.assertEqual(EXAMPLE['tag_names'], sot.tag_names)
        self.assertEqual(EXAMPLE['content'], sot.content)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
