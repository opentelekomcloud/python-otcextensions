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
from otcextensions.sdk.swr.v2 import repository
from otcextensions.sdk.swr.v2 import domain


class TestSwrProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestSwrProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestSwrOrganization(TestSwrProxy):
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


class TestSwrOrganzationPermissions(TestSwrProxy):
    def test_organization_permission_create(self):
        self.verify_create(self.proxy.create_organization_permissions,
                           organization.Permission,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_organization_permission_delete(self):
        self._verify(
            mock_method='otcextensions.sdk.swr.v2._base.Resource.'
                        '_delete',
            test_method=self.proxy.delete_organization_permissions,
            method_kwargs={
                'namespace': 'space',
                'user_ids': ['resource_id'],
            },
            expected_args=[
                self.proxy,
                ['resource_id'],
                '/manage/namespaces/space/access'
            ]),

    def test_organization_permission_update(self):
        self.verify_update(self.proxy.update_organization_permissions,
                           organization.Permission,
                           method_kwargs={
                               'namespace': 'id',
                               'permissions': [
                                   {
                                       'user_id': '123',
                                       'user_name': 'test',
                                       'user_auth': 1
                                   }
                               ],
                           },
                           method_args=[],
                           expected_kwargs={
                               'namespace': 'id',
                               'permissions': [
                                   {
                                       'user_id': '123',
                                       'user_name': 'test',
                                       'auth': 1
                                   }
                               ],
                           })

    def test_organization_permissions(self):
        self.verify_list(self.proxy.organization_permissions,
                         organization.Permission,
                         method_kwargs={
                             'namespace': 'id',
                             'permissions': [
                                 {
                                     'user_id': '123',
                                     'user_name': 'test',
                                     'auth': 1
                                 }
                             ],
                         })


class TestSwrRepository(TestSwrProxy):
    def test_repository_create(self):
        self.verify_create(self.proxy.create_repository,
                           repository.Repository,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_repository_delete(self):
        self.verify_delete(self.proxy.delete_repository,
                           repository.Repository, True,
                           method_kwargs={
                               'repository': 'resource_id'
                           },
                           expected_kwargs={
                               'namespace': 'resource_id'
                           })

    def test_repository_get(self):
        self.verify_get(self.proxy.get_repository,
                        repository.Repository,
                        method_kwargs={
                            'repository': 'resource_id'
                        },
                        expected_kwargs={
                            'namespace': 'resource_id'
                        })

    def test_repositories(self):
        self.verify_list(self.proxy.repositories,
                         repository.Repository)


class TestSwrRepositoryPermissions(TestSwrProxy):
    def test_repository_permission_create(self):
        self.verify_create(self.proxy.create_repository_permissions,
                           repository.Permission,
                           method_kwargs={
                               'namespace': 'id',
                               'permissions': [
                                   {
                                       'user_id': '123',
                                       'user_name': 'test',
                                       'user_auth': 1
                                   }
                               ],
                           },
                           method_args=[],
                           expected_kwargs={
                               'namespace': 'id',
                               'permissions': [
                                   {
                                       'user_id': '123',
                                       'user_name': 'test',
                                       'auth': 1
                                   }
                               ],
                           })

    def test_repository_permission_delete(self):
        self._verify(
            mock_method='otcextensions.sdk.swr.v2._base.Resource.'
                        '_delete',
            test_method=self.proxy.delete_repository_permissions,
            method_kwargs={
                'namespace': 'space',
                'repository': 'repo',
                'user_ids': ['resource_id'],
            },
            expected_args=[
                self.proxy,
                ['resource_id'],
                '/manage/namespaces/space/repos/repo/access'
            ]),

    def test_repository_permission_update(self):
        self.verify_update(self.proxy.update_repository_permissions,
                           repository.Permission,
                           method_kwargs={
                               'namespace': 'id',
                               'permissions': [
                                   {
                                       'user_id': '123',
                                       'user_name': 'test',
                                       'user_auth': 1
                                   }
                               ],
                           },
                           method_args=[],
                           expected_kwargs={
                               'namespace': 'id',
                               'permissions': [
                                   {
                                       'user_id': '123',
                                       'user_name': 'test',
                                       'auth': 1
                                   }
                               ],
                           })

    def test_repository_permissions(self):
        self.verify_list(self.proxy.repository_permissions,
                         repository.Permission,
                         method_kwargs={
                             'namespace': 'id',
                             'repository': 'repo',
                             'permissions': [
                                 {
                                     'user_id': '123',
                                     'user_name': 'test',
                                     'auth': 1
                                 }
                             ],
                         })


class TestSwrDomain(TestSwrProxy):
    def test_domain_create(self):
        self.verify_create(self.proxy.create_domain,
                           domain.Domain,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_domain_update(self):
        self.verify_update(self.proxy.update_domain,
                           domain.Domain,
                           method_args=[],
                           method_kwargs={
                               'namespace': 'space',
                               'repository': 'repo',
                               'access_domain': 'domain',
                               'description': 'updated',
                               'permit': 'read',
                               'deadline': 'forever'},
                           expected_kwargs={
                               'namespace': 'space',
                               'repository': 'repo',
                               'access_domain': 'domain',
                               'id': 'domain',
                               'description': 'updated',
                               'permit': 'read',
                               'deadline': 'forever'})

    def test_domain_delete(self):
        self.verify_delete(self.proxy.delete_domain,
                           domain.Domain,
                           ignore_missing=True,
                           method_kwargs={
                               'namespace': 'space',
                               'repository': 'resource_id',
                               'access_domain': 'domain',
                           },
                           expected_kwargs={
                               'repository': 'resource_id',
                               'id': 'domain',
                               'ignore_missing': True,
                               'namespace': 'space'
                           },
                           method_args=[])

    def test_domain_get(self):
        self.verify_get(self.proxy.get_domain,
                        domain.Domain,
                        method_kwargs={
                            'namespace': 'resource_id',
                            'repository': 'repo',
                            'access_domain': 'domain'
                        },
                        expected_kwargs={
                            'repository': 'repo',
                            'id': 'domain',
                            'namespace': 'resource_id'
                        },
                        method_args=[])

    def test_domains(self):
        self.verify_list(self.proxy.domains,
                         domain.Domain)


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
