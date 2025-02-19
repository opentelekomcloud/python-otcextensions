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
from otcextensions.sdk.apig.v2 import throttling_policy as tp

EXAMPLE = {
    "name": "throttle_demo",
    "created_at": "2020-07-31T08:44:02.205366118Z",
    "remark": "Total: 800 calls/second;"
              " user: 500 calls/second;"
              " app: 300 calls/second;"
              " IP address: 600 calls/second",
    "type": 1,
    "time_interval": 1,
    "ip_call_limits": 600,
    "app_call_limits": 300,
    "time_unit": "SECOND",
    "api_call_limits": 800,
    "id": "3437448ad06f4e0c91a224183116e965",
    "user_call_limits": 500,
    "enable_adaptive_control": "FALSE",
    "bind_num": 0,
    "is_inclu_special_throttle": 2
}


class TestThrottlingPolicy(base.TestCase):

    def test_basic(self):
        sot = tp.ThrottlingPolicy()
        self.assertEqual(
            '/apigw/instances/%(gateway_id)s/throttles',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertEqual('throttles', sot.resources_key)

    def test_make_it(self):
        sot = tp.ThrottlingPolicy(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['remark'], sot.remark)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['time_interval'], sot.time_interval)
