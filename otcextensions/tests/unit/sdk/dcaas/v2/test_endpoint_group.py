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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.dcaas.v2 import endpoint_group


EXAMPLE = {
    "name" : "endpoint group1",
    "description": "test description",
    "endpoints" : [ "10.2.0.0/24", "10.3.0.0/24" ],
    "tenant_id": "6fbe9263116a4b68818cf1edce16bc4f",
    "type" : "cidr"
}


class TestDirectConnectEndpointGroup(base.TestCase):

    def setUp(self):
        super(TestDirectConnectEndpointGroup, self).setUp()
        self.session = mock.Mock(spec=adapter.Adapter)
        self.session.put = mock.Mock()

    def test_basic(self):
        sot = endpoint_group.DirectConnectEndpointGroup()
        self.assertEqual('/dcaas/dc-endpoint-groups', sot.base_path)
        self.assertEqual('dc_endpoint_group', sot.resource_key)
        self.assertEqual('dc_endpoint_groups', sot.resources_key)

        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint_group.DirectConnectEndpointGroup(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['endpoints'], sot.endpoints)
        self.assertEqual(EXAMPLE['tenant_id'], sot.project_id)
        self.assertEqual(EXAMPLE['type'], sot.type)
