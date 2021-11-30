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

from otcextensions.sdk.vpc.v1 import vpc


IDENTIFIER = 'ID'
EXAMPLE = {
    "name": "vpc",
    "cidr": "192.168.200.0/24",
    "status": "CREATING",
    "description": "test",
    "tenant_id": "6fbe9263116a4b68818cf1edce16bc4f",
    "routes": [],
    "enable_shared_snat": False,
    "id": "3d42a0d4-a980-4613-ae76-a2cddecff054"
}


class TestVpc(base.TestCase):

    def setUp(self):
        super(TestVpc, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = vpc.Vpc()
        self.assertEqual('vpc', sot.resource_key)
        self.assertEqual('vpcs', sot.resources_key)
        path = '/v1/%(project_id)s/vpcs'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = vpc.Vpc(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['routes'], sot.routes)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['cidr'], sot.cidr)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['routes'], sot.routes)
        self.assertEqual(EXAMPLE['enable_shared_snat'], sot.enable_shared_snat)
