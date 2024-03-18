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
import os
import uuid

# from openstack import resource

from otcextensions.tests.functional.sdk.swr import TestSwr


class TestOrganization(TestSwr):

    def setUp(self):
        super(TestOrganization, self).setUp()

        self.org_name = "sdk-swr-org-" + uuid.uuid4().hex
        self.org = self.client.create_organization(
            namespace=self.org_name
        )
        if os.getenv("OS_SWR_PERMISSIONS_RUN"):
            self.permission = [
                {
                    "user_id": "5a23ecb3999b458d92d51d524bb7fb4b",
                    "user_name": "pgubina",
                    "auth": 1
                }
            ]
            self.org_perm = self.client.create_organization_permissions(
                namespace=self.org_name, permissions=self.permission
            )
        self.addCleanup(self.conn.swr.delete_organization, self.org_name)

    def test_list_organizations(self):
        query = {}
        orgs = list(self.client.organizations(**query))
        self.assertGreaterEqual(len(orgs), 0)

    def test_get_organization(self):
        o = self.client.get_organization(self.org.namespace)
        self.assertEqual(self.org.namespace, o.name)
        self.assertEqual(7, o.auth)

    def test_find_organization(self):
        o = self.client.find_organization(self.org_name)
        self.assertEqual(self.org.namespace, o.name)
        self.assertEqual(7, o.auth)

    def test_organization_permissions(self):
        o = list(self.client.organization_permissions(self.org.namespace))
        self.assertEqual(self.org.namespace, o[0].name)

    def test_update_organization_permissions(self):
        if os.getenv("OS_SWR_PERMISSIONS_RUN"):
            o = self.client.update_organization_permissions(
                namespace=self.org_name, permissions=[
                    {
                        "user_id": "5a23ecb3999b458d92d51d524bb7fb4b",
                        "user_name": "pgubina",
                        "auth": 3
                    }
                ]
            )
            self.assertEqual(3, o.permissions[0].auth)

    def test_delete_organization_permissions(self):
        if os.getenv("OS_SWR_PERMISSIONS_RUN"):
            orgs = self.client.delete_organization_permissions(
                self.org.namespace,
                [self.org_perm.permissions[0].user_id]
            )
            self.assertEqual(orgs, None)
