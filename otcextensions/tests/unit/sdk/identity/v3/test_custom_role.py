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
import uuid

from openstack.tests.unit import base

from otcextensions.sdk.identity.v3 import custom_role

EXAMPLE = {
    "id": uuid.uuid4().hex,
    "name": "role" + uuid.uuid4().hex[:4],
    "description": "test",
    "domain_id": uuid.uuid4().hex,
    "catalog": "CUSTOMED",
    "display_name": "custom_" + uuid.uuid4().hex[:4],
    "type": "XA",
    "created_at": "1600181033358",
    "updated_at": "1600181033358",
}


class TestCustomRole(base.TestCase):

    def setUp(self):
        super(TestCustomRole, self).setUp()

    def test_basic(self):
        sot = custom_role.CustomRole()

        self.assertEqual('/v3.0/OS-ROLE/roles', sot.base_path)
        self.assertEqual('roles', sot.resources_key)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = custom_role.CustomRole(connection=self.cloud, **EXAMPLE)
        # Check how the override with "real" connection works
        self.assertEqual(
            'https://identity.example.com/v3.0/OS-ROLE/roles',
            sot.base_path)

        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['created_at'], sot.created_at)
