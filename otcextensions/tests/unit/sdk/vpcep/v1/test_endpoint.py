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
from otcextensions.sdk.vpcep.v1 import endpoint
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = {
    'active_status': ['active'],
    'created_at': '2024-02-26T14:10:12Z',
    'description': '',
    'enable_dns': False,
    'enable_status': 'enable',
    'enable_whitelist': False,
    'endpoint_pool_id': uuid.uuid4().hex,
    'endpoint_service_id': uuid.uuid4().hex,
    'endpoint_service_name': 'eu-de.css-762-az1.' + uuid.uuid4().hex,
    'id': uuid.uuid4().hex,
    'ip': '192.168.0.232',
    'marker_id': 16952019,
    'project_id': uuid.uuid4().hex,
    'routetables': [],
    'service_type': 'interface',
    'specification_name': 'default',
    'status': 'accepted',
    'subnet_id': uuid.uuid4().hex,
    'tags': [
        {
            'key': 'test1',
            'value': 'test1',
        }
    ],
    'updated_at': '2024-02-26T14:10:14Z',
    'vpc_id': uuid.uuid4().hex,
    'whitelist': [],
}


class TestEndpoint(base.TestCase):

    def test_basic(self):
        sot = endpoint.Endpoint()
        self.assertEqual('endpoints', sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('/vpc-endpoints', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

        self.assertDictEqual(
            {
                'id': 'id',
                'limit': 'limit',
                'router_id': 'vpc_id',
                'marker': 'marker',
                'offset': 'offset',
                'endpoint_service_name': 'endpoint_service_name',
                'sort_key': 'sort_key',
                'sort_dir': 'sort_dir',
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        updated_sot_attrs = {
            'enable_dns': 'is_dns_enabled',
            'enable_whitelist': 'is_whitelist_enabled',
            'routetables': 'route_tables',
            'vpc_id': 'router_id',
            'subnet_id': 'network_id',
        }
        sot = endpoint.Endpoint(**EXAMPLE)
        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs.keys():
                self.assertEqual(
                    getattr(sot, updated_sot_attrs[key]), EXAMPLE[key]
                )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)
