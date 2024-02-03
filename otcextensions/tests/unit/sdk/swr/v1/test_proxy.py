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
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.swr.v2 import _proxy
from otcextensions.sdk.swr.v2 import organization


class TestSwrProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestSwrProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSwrOrganzation(TestSwrProxy):
    def test_organization_create(self):
        self.verify_create(self.proxy.create_organization,
                           organization.Organization,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_organization_delete(self):
        self.verify_delete(self.proxy.delete_organization,
                           organization.Organization, True)

    def test_organization_get(self):
        self.verify_get(self.proxy.get_organization,
                        organization.Organization)

    def test_organizations(self):
        self.verify_list(self.proxy.organizations,
                         organization.Organization)


class TestExtractName(TestSwrProxy):

    def test_extract_name(self):
        self.assertEqual(
            [],
            self.proxy._extract_name('/v2')
        )

        self.assertEqual(
            ['manage', 'shared-repositories'],
            self.proxy._extract_name(
                '/v2/manage/shared-repositories')
        )
        self.assertEqual(
            ['manage', 'repos'],
            self.proxy._extract_name('/v2/manage/repos')
        )
        self.assertEqual(
            ['manage', 'namespaces'],
            self.proxy._extract_name('/v2/manage/namespaces')
        )
