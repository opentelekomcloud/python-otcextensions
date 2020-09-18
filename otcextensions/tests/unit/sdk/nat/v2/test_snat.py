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

from otcextensions.sdk.nat.v2 import snat


INSTANCE_ID = '5b95c675-69c2-4656-ba06-58ff72e1d338'
EXAMPLE = {
    'floating_ip_id': 'bdc10a4c-d81a-41ec-adf7-de857f7c812a',
    'status': 'PENDING_CREATE',
    'nat_gateway_id': 'a78fb3eb-1654-4710-8742-3fc49d5f04f8',
    'admin_state_up': True,
    'network_id': 'eaad9cd6-2372-4be1-9535-9bd37210ae7b',
    'cidr': None,
    'source_type': 0,
    'project_id': '27e25061336f4af590faeabeb7fcd9a3',
    'created_at': '2017-11-18 07:54:21.665430',
    'id': INSTANCE_ID,
    'floating_ip_address': '5.21.11.226'
}


class TestSnat(base.TestCase):

    def test_basic(self):
        sot = snat.Snat()
        self.assertEqual('snat_rule', sot.resource_key)
        self.assertEqual('snat_rules', sot.resources_key)
        path = '/snat_rules'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = snat.Snat(**EXAMPLE)
        self.assertEqual(EXAMPLE['floating_ip_id'], sot.floating_ip_id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['nat_gateway_id'], sot.nat_gateway_id)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.admin_state_up)
        self.assertEqual(EXAMPLE['network_id'], sot.network_id)
        self.assertIsNone(sot.cidr)
        self.assertEqual(EXAMPLE['source_type'], sot.source_type)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['floating_ip_address'],
                         sot.floating_ip_address)
