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
from otcextensions.sdk.vpcep.v1 import target_service
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal


EXAMPLE = {
    "id": "9d4c1028-1336-4556-9881-b5d807c1b8a8",
    "service_name": "test123",
    "service_type": "interface",
    "created_at": "2018-09-17T07:28:31Z",
    "is_charge": "true"
}


class TestTargetService(base.TestCase):

    def test_basic(self):
        sot = target_service.TargetService()
        self.assertEqual(None, sot.resources_key)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual('/vpc-endpoint-services/describe', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

        self.assertDictEqual(
            {
                'id': 'id',
                'limit': 'limit',
                'marker': 'marker',
                'name': 'endpoint_service_name',
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = target_service.TargetService(**EXAMPLE)
        assert_attributes_equal(self, sot, EXAMPLE)
