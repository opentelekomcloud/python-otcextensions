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

from otcextensions.sdk.cts.v1 import tracker

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "bucket_name": "my_created_bucket",
    "tracker_name": "system",
    "detail": "noBucket",
    "file_prefix_name": "some_folder",
    "status": "disabled",
    "smn": {
        "is_support_smn": False,
        "topic_id": "urn:smn:regionId:someid:cts-test",
        "is_send_all_key_operation": False,
        "operations": ["delete", "create", "login"],
        "need_notify_user_list": ["user1", "user2"]
    }
}


class TestTracker(base.TestCase):

    def test_basic(self):
        sot = tracker.Tracker()

        self.assertEqual('/tracker', sot.base_path)

        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):

        sot = tracker.Tracker(**EXAMPLE)
        self.assertEqual(EXAMPLE['bucket_name'], sot.bucket_name)
        self.assertEqual(EXAMPLE['tracker_name'], sot.name)
        self.assertEqual(EXAMPLE['detail'], sot.detail)
        self.assertEqual(EXAMPLE['file_prefix_name'], sot.file_prefix_name)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['smn']['is_support_smn'], sot.smn.enabled)
        self.assertEqual(EXAMPLE['smn']['topic_id'], sot.smn.topic_id)
        self.assertEqual(
            EXAMPLE['smn']['is_send_all_key_operation'],
            sot.smn.is_send_all_key_operation)
        self.assertEqual(EXAMPLE['smn']['operations'], sot.smn.operations)
        self.assertEqual(
            EXAMPLE['smn']['need_notify_user_list'],
            sot.smn.notify_users)
