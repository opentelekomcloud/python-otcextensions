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
from otcextensions.sdk.ctsv3.v3 import key_event

EXAMPLE = {
    "notification_name": "test",
    "operation_type": "complete",
    "topic_id": "urn:smn:{regionid}:24edf66e79d04187acb99a463e610764:test"
}


class TestKeyEvent(base.TestCase):
    def test_basic(self):
        sot = key_event.KeyEvent()
        self.assertEqual('/notifications', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = key_event.KeyEvent(**EXAMPLE)
        self.assertEqual(EXAMPLE['notification_name'], sot.notification_name)
        self.assertEqual(EXAMPLE['operation_type'], sot.operation_type)
        self.assertEqual(EXAMPLE['topic_id'], sot.topic_id)
