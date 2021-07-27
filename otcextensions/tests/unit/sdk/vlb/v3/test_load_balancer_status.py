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

from otcextensions.sdk.vlb.v3 import load_balancer_status

EXAMPLE = {
    'loadbalancer_id': 'id',
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = load_balancer_status.LoadBalancerStatus()
        path = '/elb/loadbalancers/%(loadbalancer_id)s/statuses'
        self.assertEqual(path, sot.base_path)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = load_balancer_status.LoadBalancerStatus(**EXAMPLE)
        self.assertEqual(EXAMPLE['loadbalancer_id'], sot.loadbalancer_id)
