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

from otcextensions.sdk.deh.v1 import server


FAKE_ID = '68d5745e-6af2-40e4-945d-fe449be00148'
EXAMPLE = {
    'addresses': {
        '68269e6e-4a27-441b-8029-35373ad50bd9': [
            {
                'addr': '192.168.0.3',
                'version': 4
            }
        ]
    },
    'created': '2012-09-07T16:56:37Z',
    'flavor': {
        'id': '1'
    },
    'id': FAKE_ID,
    'metadata': {
        'os_type': 'Linux'
    },
    'name': 'new-server-test',
    'status': 'ACTIVE',
    'tenant_id': 'openstack',
    'updated': '2012-09-07T16:56:37Z',
    'user_id': 'fake'
}


class TestHost(base.TestCase):

    def test_basic(self):
        sot = server.Server()

        self.assertEqual('/dedicated-hosts/%(dedicated_host_id)s/servers',
                         sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_get)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_update)

    def test_make_it(self):

        sot = server.Server(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], FAKE_ID)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['flavor'], sot.flavor)
        self.assertEqual(EXAMPLE['metadata'], sot.metadata)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['tenant_id'], sot.tenant_id)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['user_id'], sot.user_id)
