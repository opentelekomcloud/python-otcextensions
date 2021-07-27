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

from otcextensions.sdk.vlb.v3 import load_balancer

EXAMPLE = {
    'name': 'example',
    'description': 'example',
    'vip_subnet_cidr_id': 'subnet_id',
    'vpc_id': 'router_id',
    'elb_virsubnet_ids': 'network_id',
    'admin_state_up': True,
    'guaranteed': True,
    'provider': 'vlb',
    'availability_zone_list': ['eu-nl-01'],
    'publicip': {
        "network_type": "5_bgp",
        "billing_info": "",
        "bandwidth": {
            "size": 2,
            "share_type": "PER",
            "charge_mode": "traffic",
            "name": "elbv3_eip_traffic"
        }
    },
    'ip_target_enable': True,
    'tags': [{
        "key": "test",
        "value": "api"
    }],
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = load_balancer.LoadBalancer()
        path = '/elb/loadbalancers'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = load_balancer.LoadBalancer(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['availability_zone_list'], sot.availability_zones)
        self.assertEqual(EXAMPLE['publicip'], sot.floating_ip[0])
