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

from otcextensions.sdk.identity.v3 import agency_role


FAKE_ID = "945d-fe449be00148"
EXAMPLE = {
    "catalog": "BASE",
    "display_name": "Tenant Guest",
    "name": "readonly",
    "policy": {},
    "domain_id": None,
    "type": "AA",
    "id": "b32d99a7778d4fd9aa5bc616c3dc4e5f",
    "description": "Tenant Guest"
}


class TestAgencyRole(base.TestCase):

    def setUp(self):
        super(TestAgencyRole, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.post = mock.Mock()

    def test_basic(self):
        sot = agency_role.AgencyRole()

        self.assertEqual(
            ('/v3.0/OS-AGENCY/%(role_ref_type)ss'
             '/%(role_ref_id)s/agencies/%(agency_id)s/roles'),
            sot.base_path)
        self.assertEqual('roles', sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_head)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):

        sot = agency_role.AgencyRole(connection=self.cloud, **EXAMPLE)
        # Check how the override with "real" connection works
        self.assertEqual(
            ('https://identity.example.com/v3.0/OS-AGENCY/%(role_ref_type)ss'
             '/%(role_ref_id)s/agencies/%(agency_id)s/roles'),
            sot.base_path)

        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['description'], sot.description)
