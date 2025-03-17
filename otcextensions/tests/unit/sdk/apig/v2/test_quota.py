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
from otcextensions.sdk.apig.v2 import quota


EXAMPLE_QUOTA = {
    'gateway_id': 'gateway-67890',
    'app_id': 'app-12345',
    'app_quota_id': 'quota-123',
    'name': 'Test Quota',
    'call_limits': 1000,
    'time_unit': 'minute',
    'time_interval': 60,
    'remark': 'This is a test quota',
    'reset_time': '2025-02-07T12:00:00Z',
    'create_time': '2025-02-07T12:30:00Z',
    'bound_app_num': 5
}


class TestQuota(base.TestCase):

    def test_basic(self):
        sot = quota.Quota()
        self.assertEqual('/apigw/instances/%(gateway_id)s/apps/'
                         '%(app_id)s/bound-quota',
                         sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = quota.Quota(**EXAMPLE_QUOTA)
        self.assertEqual(EXAMPLE_QUOTA['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_QUOTA['app_id'], sot.app_id)
        self.assertEqual(EXAMPLE_QUOTA['app_quota_id'], sot.app_quota_id)
        self.assertEqual(EXAMPLE_QUOTA['name'], sot.name)
        self.assertEqual(EXAMPLE_QUOTA['call_limits'], sot.call_limits)
        self.assertEqual(EXAMPLE_QUOTA['time_unit'], sot.time_unit)
        self.assertEqual(EXAMPLE_QUOTA['time_interval'], sot.time_interval)
        self.assertEqual(EXAMPLE_QUOTA['remark'], sot.remark)
        self.assertEqual(EXAMPLE_QUOTA['reset_time'], sot.reset_time)
        self.assertEqual(EXAMPLE_QUOTA['create_time'], sot.create_time)
        self.assertEqual(EXAMPLE_QUOTA['bound_app_num'], sot.bound_app_num)
