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

from otcextensions.sdk.nat.v2 import dnat


INSTANCE_ID = '5b95c675-69c2-4656-ba06-58ff72e1d338'
EXAMPLE = {
    'floating_ip_id': 'bdc10a4c-d81a-41ec-adf7-de857f7c812a',
    'status': 'ACTIVE',
    'nat_gateway_id': 'a78fb3eb-1654-4710-8742-3fc49d5f04f8',
    'admin_state_up': True,
    'port_id': '9a469561-daac-4c94-88f5-39366e5ea193',
    'internal_service_port': 993,
    'protocol': 'TCP',
    'project_id': '27e25061336f4af590faeabeb7fcd9a3',
    'created_at': '2017-11-18 07:54:21.665430',
    'id': INSTANCE_ID,
    'floating_ip_address': '5.21.11.226',
    'external_service_port': 242,
    'private_ip': "",
}


class TestDnat(base.TestCase):

    def test_basic(self):
        sot = dnat.Dnat()
        self.assertEqual('dnat_rule', sot.resource_key)
        self.assertEqual('dnat_rules', sot.resources_key)
        path = '/dnat_rules'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = dnat.Dnat(**EXAMPLE)
        self.assertEqual(EXAMPLE['floating_ip_id'], sot.floating_ip_id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['nat_gateway_id'], sot.nat_gateway_id)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.admin_state_up)
        self.assertEqual(EXAMPLE['port_id'], sot.port_id)
        self.assertEqual(EXAMPLE['internal_service_port'],
                         sot.internal_service_port)
        self.assertEqual(EXAMPLE['protocol'], sot.protocol)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['floating_ip_address'],
                         sot.floating_ip_address)
        self.assertEqual(EXAMPLE['external_service_port'],
                         sot.external_service_port)
        self.assertEqual(EXAMPLE['private_ip'], sot.private_ip)
