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
    'availability_zone_list': ['eu-nl-01'],
    'created_at': 'created_at',
    'description': 'description',
    'deletion_protection_enable': True,
    'eips': [{
        'eip_id': 'eip_id',
        'eip_address': 'eip_address',
        'ip_version': 'ip_version'
    }],
    'publicips': [{
        'eip_id': 'eip_id',
        'eip_address': 'eip_address',
        'ip_version': 'ip_version'
    }],
    'guaranteed': True,
    'admin_state_up': True,
    'ip_target_enable': True,
    'l4_flavor_id': 'l4_flavor_id',
    'l7_flavor_id': 'l7_flavor_id',
    'listeners': [{'id': 'lstnr_id_1'}, {'id': 'lstnr_id_2'}],
    'elb_virsubnet_ids': ['uuid1', 'uuid2'],
    'elb_virsubnet_type': 'subnet_type',
    'operating_status': 'operating_status',
    'pools': [{'id': 'pool_id_1'}, {'id': 'pool_id_2'}],
    'project_id': 'project_id',
    'provider': 'provider',
    'provisioning_status': 'provisioning_status',
    'tags': [{
        "key": "key1",
        "value": "value1"
    }],
    'updated_at': 'updated_at',
    'vip_address': 'vip_address',
    'vip_port_id': 'vip_port_id',
    'vip_subnet_cidr_id': 'vip_subnet_id',
    'vpc_id': 'vpc_id',
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
        self.assertEqual(EXAMPLE['availability_zone_list'],
                         sot.availability_zones)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['deletion_protection_enable'], sot.deletion_protection_enable)
        self.assertEqual(EXAMPLE['eips'], sot.eips)
        self.assertEqual(EXAMPLE['publicips'], sot.floating_ips)
        self.assertEqual(EXAMPLE['guaranteed'], sot.is_guaranteed)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.is_admin_state_up)
        self.assertEqual(EXAMPLE['ip_target_enable'], sot.ip_target_enable)
        self.assertEqual(EXAMPLE['l4_flavor_id'], sot.l4_flavor_id)
        self.assertEqual(EXAMPLE['l7_flavor_id'], sot.l7_flavor_id)
        self.assertEqual(EXAMPLE['listeners'], sot.listeners)
        self.assertEqual(EXAMPLE['elb_virsubnet_ids'], sot.network_ids)
        self.assertEqual(EXAMPLE['elb_virsubnet_type'], sot.subnet_type)
        self.assertEqual(EXAMPLE['operating_status'], sot.operating_status)
        self.assertEqual(EXAMPLE['pools'], sot.pools)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['provider'], sot.provider)
        self.assertEqual(EXAMPLE['provisioning_status'], sot.provisioning_status)
        self.assertEqual(EXAMPLE['tags'], sot.tags)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)

        self.assertEqual(EXAMPLE['vip_address'], sot.vip_address)
        self.assertEqual(EXAMPLE['vip_port_id'], sot.vip_port_id)
        self.assertEqual(EXAMPLE['vip_subnet_cidr_id'], sot.vip_subnet_id)
        self.assertEqual(EXAMPLE['vpc_id'], sot.vpc_id)
