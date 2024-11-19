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
from openstack.tests.unit import base
from otcextensions.sdk.vpcep.v1 import public_service
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal


EXAMPLE = {
    "id": "b0e22f6f-26f4-461c-b140-d873464d4fa0",
    "owner": "example",
    "service_name": "test123",
    "service_type": "interface",
    "created_at": "2018-09-10T13:13:23Z",
    "is_charge": "true"
}


class TestPublicService(base.TestCase):
    def test_basic(self):
        sot = public_service.PublicService()
        self.assertEqual('endpoint_services', sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('/vpc-endpoint-services/public', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

        self.assertDictEqual(
            {
                'id': 'id',
                'limit': 'limit',
                'marker': 'marker',
                'offset': 'offset',
                'name': 'endpoint_service_name',
                'sort_key': 'sort_key',
                'sort_dir': 'sort_dir',
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = public_service.PublicService(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)
