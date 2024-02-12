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


class TestDomain(TestSwr):

    def setUp(self):
        super(TestDomain, self).setUp()

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
            is_public=False,
        )
        self.domain = self.client.create_domain(
            namespace=self.org_name,
            repository=self.repo_name,
            access_domain='OTC00000000001000000447',
            permit='read',
            deadline='forever',
            description='desc'
        )

    def tearDown(self):
        super(TestDomain, self).tearDown()
        self.repo = self.client.delete_domain(
            namespace=self.org_name,
            repository=self.repo_name,
            access_domain=self.domain.access_domain,
        )
        self.conn.swr.delete_repository(
            self.org_name,
            self.repo_name
        )
        self.conn.swr.delete_organization(self.org_name)

    def test_list_domains(self):
        domains = list(self.client.domains(
            namespace=self.org.namespace,
            repository=self.repo_name
        ))
        self.assertGreaterEqual(len(domains), 0)

    def test_update_domain(self):
        update = self.client.update_domain(
            namespace=self.org_name,
            repository=self.repo_name,
            access_domain=self.domain.access_domain,
            description='updated',
            permit='read',
            deadline='forever',

        )
        self.assertEqual(update.description, 'updated')

    def test_get_domain(self):
        domain = self.client.get_domain(
            self.org.namespace,
            self.repo_name,
            self.domain.access_domain,
        )
        self.assertGreaterEqual(domain.exist, True)
