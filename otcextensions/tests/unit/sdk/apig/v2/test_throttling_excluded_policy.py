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
from otcextensions.sdk.apig.v2 import throttling_excluded as tx

EXAMPLE = {
    "call_limits": 200,
    "app_name": "app_demo",
    "object_name": "app_demo",
    "object_id": "356de8eb7a8742168586e5daf5339965",
    "throttle_id": "3437448ad06f4e0c91a224183116e965",
    "apply_time": "2020-08-04T02:40:56Z",
    "id": "a3e9ff8db55544ed9db91d8b048770c0",
    "app_id": "356de8eb7a8742168586e5daf5339965",
    "object_type": "APP"
}


class TestThrottlingPolicy(base.TestCase):

    def test_basic(self):
        sot = tx.ThrottlingExcludedPolicy()
        self.assertEqual(
            f'/apigw/instances/%(gateway_id)s/throttles/'
            f'%(throttle_id)s/throttle-specials',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertEqual('throttle_specials', sot.resources_key)

    def test_make_it(self):
        sot = tx.ThrottlingExcludedPolicy(**EXAMPLE)
        self.assertEqual(EXAMPLE['call_limits'], sot.call_limits)
        self.assertEqual(EXAMPLE['app_name'], sot.app_name)
        self.assertEqual(EXAMPLE['object_name'], sot.object_name)
        self.assertEqual(EXAMPLE['object_id'], sot.object_id)
        self.assertEqual(EXAMPLE['throttle_id'], sot.throttle_id)
