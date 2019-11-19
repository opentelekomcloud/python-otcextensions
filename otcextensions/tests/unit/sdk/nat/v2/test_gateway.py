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

from otcextensions.sdk.nat.v2 import gateway


INSTANCE_NAME = 'GATEWAYNAME'
INSTANCE_ID = 'a78fb3eb-1654-4710-8742-3fc49d5f04f8'
EXAMPLE = {
    'router_id': 'd84f345c-80a1-4fa2-a39c-d0d397c3f09a',
    'status': 'PENDING_CREATE',
    'description': 'Test Gateway Response',
    'admin_state_up': True,
    'tenant_id': '27e25061336f4af590faeabeb7fcd9a3',
    'created_at': '2017-11-18 07:34:32.203044',
    'spec': '2',
    'internal_network_id': '89d66639-aacb-4929-969d-07080b0f9fd9',
    'id': INSTANCE_ID,
    'name': INSTANCE_NAME
}


class TestGateway(base.TestCase):

    def test_basic(self):
        sot = gateway.Gateway()
        self.assertEqual('nat_gateway', sot.resource_key)
        self.assertEqual('nat_gateways', sot.resources_key)
        path = '/nat_gateways'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = gateway.Gateway(**EXAMPLE)
        self.assertEqual(EXAMPLE['router_id'], sot.router_id)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['admin_state_up'], sot.admin_state_up)
        self.assertEqual(EXAMPLE['tenant_id'], sot.tenant_id)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
        self.assertEqual(EXAMPLE['spec'], sot.spec)
        self.assertEqual(EXAMPLE['internal_network_id'],
                         sot.internal_network_id)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
