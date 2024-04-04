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
#
import uuid

from openstack.tests.unit import base
from otcextensions.sdk.vpcep.v1 import service
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = {
    'id': uuid.uuid4().hex,
    'port_id': uuid.uuid4().hex,
    'vpc_id': uuid.uuid4().hex,
    'pool_id': uuid.uuid4().hex,
    'status': 'available',
    'approval_enabled': False,
    'service_name': 'test123',
    'service_type': 'interface',
    'server_type': 'VM',
    'project_id': uuid.uuid4().hex,
    'created_at': '2018-01-30T07:42:01.174',
    'ports': [
        {'client_port': 8080, 'server_port': 90, 'protocol': 'TCP'},
        {'client_port': 8081, 'server_port': 80, 'protocol': 'TCP'},
    ],
}


class TestEndpointService(base.TestCase):

    def setUp(self):
        super(TestEndpointService, self).setUp()

    def test_basic(self):
        sot = service.Service()
        self.assertEqual('endpoint_services', sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('/vpc-endpoint-services', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

        self.assertDictEqual(
            {
                'id': 'id',
                'limit': 'limit',
                'marker': 'marker',
                'name': 'endpoint_service_name',
                'offset': 'offset',
                'sort_dir': 'sort_dir',
                'sort_key': 'sort_key',
                'status': 'status',
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = service.Service(**EXAMPLE)
        updated_sot_attrs = {
            'approval_enabled': 'is_approval_enabled',
            'vpc_id': 'router_id',
        }
        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs.keys():
                self.assertEqual(
                    getattr(sot, updated_sot_attrs[key]), EXAMPLE[key]
                )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)
