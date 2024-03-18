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

from otcextensions.tests.functional.sdk.swr import TestSwr


class TestRepository(TestSwr):

    def setUp(self):
        super(TestRepository, self).setUp()

        self.org_name = "sdk-swr-org-" + uuid.uuid4().hex
        self.repo_name = "sdk-swr-repo-" + uuid.uuid4().hex
        self.org = self.client.create_organization(
            namespace=self.org_name
        )
        self.repo = self.client.create_repository(
            namespace=self.org_name,
            repository=self.repo_name,
            category='linux',
            description='this is a acc test repository',
            is_public=True,
        )
        if os.getenv("OS_SWR_PERMISSIONS_RUN"):
            self.permission = [
                {
                    "user_id": "5a23ecb3999b458d92d51d524bb7fb4b",
                    "user_name": "pgubina",
                    "auth": 1
                }
            ]
            self.repo_perm = self.client.create_repository_permissions(
                namespace=self.org_name,
                repository=self.repo_name,
                permissions=self.permission
            )

    def tearDown(self):
        super(TestRepository, self).tearDown()
        if os.getenv("OS_SWR_PERMISSIONS_RUN"):
            self.client.delete_repository_permissions(
                namespace=self.org.namespace,
                repository=self.repo.repository,
                user_ids=[self.repo_perm.permissions[0].user_id]
            )
        self.conn.swr.delete_repository(
            self.org_name,
            self.repo_name
        )
        self.conn.swr.delete_organization(self.org_name)

    def test_get_repository(self):
        repo = self.client.get_repository(
            namespace=self.org.namespace,
            repository=self.repo_name
        )
        self.assertEqual(self.repo_name, repo.name)
        self.assertEqual(True, repo.is_public)
        self.assertEqual(self.org_name, repo.namespace)

    def test_list_repositories(self):
        query = {
            'namespace': self.org.namespace
        }
        repos = list(self.client.repositories(**query))
        self.assertGreaterEqual(len(repos), 0)

    def test_update_repository(self):
        desc = 'this is a acc test repository updated'
        updated = self.client.update_repository(
            namespace=self.org_name,
            repository=self.repo_name,
            category='windows',
            description=desc,
        )
        self.assertEqual(desc, updated.description)

    def test_repository_permissions(self):
        o = list(self.client.repository_permissions(
            self.org.namespace,
            self.repo.repository
        ))
        self.assertEqual(self.org.namespace, o[0].namespace)

    def test_update_repository_permissions(self):
        if os.getenv("OS_SWR_PERMISSIONS_RUN"):
            o = self.client.update_repository_permissions(
                namespace=self.org_name,
                repository=self.repo_name,
                permissions=[
                    {
                        "user_id": "5a23ecb3999b458d92d51d524bb7fb4b",
                        "user_name": "pgubina",
                        "auth": 3
                    }
                ]
            )
            self.assertEqual(3, o.permissions[0].auth)
