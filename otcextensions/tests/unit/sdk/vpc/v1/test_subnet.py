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
from unittest import mock

from keystoneauth1 import adapter
from openstack.tests.unit import base

from otcextensions.sdk.vpc.v1 import subnet

IDENTIFIER = 'ID'
EXAMPLE = {
    'id': '4779ab1c-7c1a-44b1-a02e-93dfc361b32d',
    'name': 'subnet',
    'description': '',
    'cidr': '192.168.20.0/24',
    'dnsList': [
        '8.8.8.8',
        '1.1.1.1'
    ],
    'status': 'ACTIVE',
    'vpc_id': '3ec3b33f-ac1c-4630-ad1c-7dba1ed79d85',
    'gateway_ip': '192.168.20.1',
    'dhcp_enable': True,
    'primary_dns': '8.8.8.8',
    'secondary_dns': '1.1.1.1',
    'availability_zone': 'eu-de-01',
    'neutron_network_id': '4779ab1c-7c1a-44b1-a02e-93dfc361b32d',
    'neutron_subnet_id': '213cb9d-3122-2ac1-1a29-91ffc1231a12',
    'extra_dhcp_opts': [
        {
            'opt_value': '10.100.0.33,10.100.0.34',
            'opt_name': 'ntp'
        }
    ]
}


class TestVpc(base.TestCase):

    def setUp(self):
        super(TestVpc, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = subnet.Subnet()
        self.assertEqual('subnet', sot.resource_key)
        self.assertEqual('subnets', sot.resources_key)
        path = '/v1/%(project_id)s/subnets'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = subnet.Subnet(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['cidr'], sot.cidr)
        self.assertEqual(EXAMPLE['dnsList'], sot.dns_list)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['vpc_id'], sot.vpc_id)
        self.assertEqual(EXAMPLE['gateway_ip'], sot.gateway_ip)
        self.assertEqual(EXAMPLE['dhcp_enable'], sot.dhcp_enable)
        self.assertEqual(EXAMPLE['primary_dns'], sot.primary_dns)
        self.assertEqual(EXAMPLE['secondary_dns'], sot.secondary_dns)
        self.assertEqual(EXAMPLE['availability_zone'], sot.availability_zone)
        self.assertEqual(EXAMPLE['neutron_network_id'], sot.neutron_network_id)
        self.assertEqual(EXAMPLE['neutron_subnet_id'], sot.neutron_subnet_id)

        self.assertDictEqual(EXAMPLE['extra_dhcp_opts'][0],
                             sot.extra_dhcp_opts[0].to_dict(ignore_none=True))
