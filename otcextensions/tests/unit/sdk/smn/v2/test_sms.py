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

from otcextensions.sdk.smn.v2 import sms


EXAMPLE = {
    "message_id": "bf94b63a5dfb475994d3ac34664e24f2",
    "request_id": "9974c07f6d554a6d827956acbeb4be5f"
}


class TestSms(base.TestCase):

    def test_basic(self):
        sot = sms.Sms()
        path = '/notifications/sms'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = sms.Sms(**EXAMPLE)
        self.assertEqual(EXAMPLE['message_id'], sot.message_id)
        self.assertEqual(EXAMPLE['request_id'], sot.request_id)
