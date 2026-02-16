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

from otcextensions.sdk.natv3.v3 import gateway


INSTANCE_ID = '14338426-6afe-4019-996b-3a9525296e11'
PROJECT_ID = '70505c941b9b4dfd82fd351932328a2f'
DOWNLINK_VPC = {
    'vpc_id': '3cb66d44-9f75-4237-bfff-e37b14d23ad2',
    'virsubnet_id': '373979ee-f4f0-46c5-80e3-0fbf72646b70',
    'ngport_ip_address': '10.0.0.17'
}
TAGS = {'key': 'key1', 'value': 'value1'}
EXAMPLE = {
    'id': INSTANCE_ID,
    'name': 'private-nat-gateway-name1',
    'description': 'private-nat-gateway-description1',
    'spec': 'Small',
    'project_id': PROJECT_ID,
    'enterprise_project_id': '2759da7b-8015-404c-ae0a-a389007b0e2a',
    'status': 'ACTIVE',
    'created_at': '2019-04-22T08:47:13',
    'updated_at': '2019-04-22T08:47:13',
    'tags': [TAGS],
    'downlink_vpcs': [DOWNLINK_VPC],
    'transit_ip_pool_size_max': 1,
    'rule_max': 20
}


class TestPrivateNatGateway(base.TestCase):

    def test_basic(self):
        sot = gateway.PrivateNatGateway()
        self.assertEqual('gateways', sot.resources_key)
        self.assertEqual('gateway', sot.resource_key)
        self.assertEqual('/v3/%(project_id)s/private-nat/gateways',
                         sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = gateway.PrivateNatGateway(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['spec'], sot.spec)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['updated_at'], sot.updated_at)
        self.assertEqual(1, len(sot.downlink_vpcs))
        self.assertIsInstance(sot.downlink_vpcs[0], gateway.DownlinkVpc)
        self.assertEqual(DOWNLINK_VPC['vpc_id'], sot.downlink_vpcs[0].vpc_id)
        self.assertEqual(DOWNLINK_VPC['virsubnet_id'],
                         sot.downlink_vpcs[0].virsubnet_id)
        self.assertEqual(DOWNLINK_VPC['ngport_ip_address'],
                         sot.downlink_vpcs[0].ngport_ip_address)
        self.assertEqual(1, len(sot.tags))
        self.assertIsInstance(sot.tags[0], gateway.Tag)
        self.assertEqual(TAGS['key'], sot.tags[0].key)
        self.assertEqual(TAGS['value'], sot.tags[0].value)
        self.assertEqual(EXAMPLE['enterprise_project_id'],
                         sot.enterprise_project_id)
        self.assertEqual(EXAMPLE['rule_max'], sot.rule_max)
        self.assertEqual(EXAMPLE['transit_ip_pool_size_max'],
                         sot.transit_ip_pool_size_max)
