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

# from openstack import resource

from otcextensions.tests.functional.sdk.swr import TestSwr


class TestOrganization(TestSwr):

    def setUp(self):
        super(TestOrganization, self).setUp()

        self.org_name = "sdk-swr-org-" + uuid.uuid4().hex
        self.org = self.client.create_organization(
            organization=self.org_name
        )

        self.addCleanup(self.conn.swr.delete_organization, self.org_name)

    def test_list_organizations(self):
        query = {}
        orgs = list(self.client.organizations(**query))
        self.assertGreaterEqual(len(orgs), 0)

    def test_get_organization(self):
        o = self.client.get_organization(self.org.organization)
        self.assertEqual(self.org.organization, o.name)
        self.assertEqual(7, o.auth)

    def test_find_organization(self):
        o = self.client.find_organization(self.org_name)
        self.assertEqual(self.org.organization, o.name)
        self.assertEqual(7, o.auth)
