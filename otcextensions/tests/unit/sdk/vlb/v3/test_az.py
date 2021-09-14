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

from otcextensions.sdk.vlb.v3 import availability_zone

EXAMPLE = {
    'code': 'az1',
    'state': 'ACTIVE',
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = availability_zone.AvailabilityZone()
        path = '/elb/availability-zones'
        self.assertEqual(path, sot.base_path)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = availability_zone.AvailabilityZone(**EXAMPLE)
        self.assertEqual(EXAMPLE['code'], sot.code)
        self.assertEqual(EXAMPLE['state'], sot.state)
