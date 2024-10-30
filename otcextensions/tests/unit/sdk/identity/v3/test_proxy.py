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
import requests
from unittest import mock

from otcextensions.sdk.identity.v3 import _proxy
from otcextensions.sdk.identity.v3 import credential
from otcextensions.sdk.identity.v3 import custom_role
from otcextensions.sdk.identity.v3 import agency
from otcextensions.sdk.identity.v3 import agency_role

from openstack.tests.unit import test_proxy_base


class FakeResponse:
    def __init__(self, response, status_code=200, headers=None):
        self.body = response
        self.status_code = status_code
        headers = headers if headers else {'content-type': 'application/json'}
        self.headers = requests.structures.CaseInsensitiveDict(headers)

    def json(self):
        return self.body


class TestIdentityProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestIdentityProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestIdentityCredential(TestIdentityProxy):
    def test_credential_create(self):
        self.verify_create(self.proxy.create_credential, credential.Credential,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id',
                                            'prepend_key': True})

    def test_credential_delete(self):
        self.verify_delete(self.proxy.delete_credential,
                           credential.Credential, True)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_credential_find(self, epo_mock):
        self.verify_find(self.proxy.find_credential, credential.Credential)

    def test_credential_get(self):
        self.verify_get(self.proxy.get_credential, credential.Credential)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_credentials(self, epo_mock):
        self.verify_list(
            self.proxy.credentials,
            credential.Credential,
        )
        epo_mock.assert_called_with()

    def test_credential_update(self):
        self.verify_update(self.proxy.update_credential, credential.Credential)


class TestIdentityAgency(TestIdentityProxy):
    def test__agencynormalize_domain(self):
        with mock.patch.object(self.proxy, 'session') as s_mock:
            access_mock = mock.Mock()
            access_mock.domain_id = 'fake_domain'
            s_mock.auth = mock.Mock()
            s_mock.auth.get_auth_ref = mock.Mock(
                return_value=access_mock
            )

            self.assertDictEqual({
                'domain_id': 'fake_domain'
            }, self.proxy._agency_normalize_domain_id()
            )

    def test_agency_create(self):
        self.verify_create(self.proxy.create_agency, agency.Agency,
                           method_kwargs={'name': 'id', 'domain_id': 'fake'},
                           expected_kwargs={'name': 'id',
                                            'domain_id': 'fake',
                                            'prepend_key': True})

    def test_agency_delete(self):
        self.verify_delete(self.proxy.delete_agency,
                           agency.Agency, True)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_agency_find(self, epo_mock):
        self.verify_find(
            self.proxy.find_agency, agency.Agency,
            method_kwargs={'domain_id': 'fake'},
            expected_kwargs={'domain_id': 'fake'}
        )

    def test_agency_get(self):
        self.verify_get(self.proxy.get_agency, agency.Agency)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_agencies(self, epo_mock):
        self.verify_list(
            self.proxy.agencies,
            agency.Agency,
            method_kwargs={'domain_id': 'fake'},
            expected_kwargs={'domain_id': 'fake'}
        )
        epo_mock.assert_called_with()

    def test_agency_update(self):
        self.verify_update(self.proxy.update_agency, agency.Agency)


class TestIdentityAgencyProjectRoles(TestIdentityProxy):

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource',
        return_value=agency.Agency(id='fake'))
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_agency_project_roles(self, epo_mock, gr_mock):
        self.verify_list(
            self.proxy.agency_project_roles,
            agency_role.AgencyRole,
            method_kwargs={
                'agency': 'fake_agency',
                'project_id': 'fake_project'
            },
            expected_kwargs={
                'agency_id': 'fake',
                'role_ref_type': 'project',
                'role_ref_id': 'fake_project'
            }
        )

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_check_agency_project_role(self, epo_mock, gr_mock):
        agency_fake = agency.Agency(id='fake')
        agency_role_fake = agency_role.AgencyRole(id='fake')
        gr_mock.side_effect = [
            agency_fake,
            agency_role_fake
        ]
        expected_calls = [
            mock.call(agency.Agency, 'fake_agency'),
            mock.call(
                agency_role.AgencyRole,
                {'agency_id': 'fake',
                 'role_ref_type': 'project',
                 'role_ref_id': 'fake_project',
                 'id': 'fake_role'})
        ]
        self._verify(
            'openstack.proxy.Proxy._head',
            self.proxy.check_agency_project_role,
            method_kwargs={
                'agency': 'fake_agency',
                'project_id': 'fake_project',
                'role_id': 'fake_role'
            },
            expected_args=[
                agency_role.AgencyRole,
                agency_role_fake
            ],
        )
        gr_mock.assert_has_calls(expected_calls)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_grant_agency_project_role(self, epo_mock, gr_mock):
        agency_fake = agency.Agency(id='fake')
        agency_role_fake = agency_role.AgencyRole(
            id='fake',
            role_ref_type='project',
            role_ref_id='fake_project',
            agency_id='fake')
        gr_mock.side_effect = [
            agency_fake,
            agency_role_fake,
        ]
        self._verify(
            'openstack.proxy.Proxy.put',
            self.proxy.grant_agency_project_role,
            method_kwargs={
                'agency': 'fake_agency',
                'project_id': 'fake_project',
                'role_id': 'fake_role'
            },
            expected_args=[
                'v3.0/OS-AGENCY/projects/fake_project/agencies/fake/roles/fake'
            ],
        )

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_revoke_agency_project_role(self, epo_mock, gr_mock):
        agency_fake = agency.Agency(id='fake')
        agency_role_fake = agency_role.AgencyRole(
            id='fake',
            role_ref_type='project',
            role_ref_id='fake_project',
            agency_id='fake')
        gr_mock.side_effect = [
            agency_fake,
            agency_role_fake,
        ]
        self._verify(
            'openstack.proxy.Proxy._delete',
            self.proxy.revoke_agency_project_role,
            method_kwargs={
                'agency': 'fake_agency',
                'project_id': 'fake_project',
                'role_id': 'fake_role'
            },
            expected_args=[
                agency_role.AgencyRole, agency_role_fake
            ],
        )


class TestIdentityAgencyDomainRoles(TestIdentityProxy):

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource',
        return_value=agency.Agency(id='fake'))
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_agency_domain_roles(self, epo_mock, gr_mock):
        self.verify_list(
            self.proxy.agency_domain_roles,
            agency_role.AgencyRole,
            method_kwargs={
                'agency': 'fake_agency',
                'domain_id': 'fake_domain'
            },
            expected_kwargs={
                'agency_id': 'fake',
                'role_ref_type': 'domain',
                'role_ref_id': 'fake_domain'
            }
        )

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_check_agency_domain_role(self, epo_mock, gr_mock):
        agency_fake = agency.Agency(id='fake')
        agency_role_fake = agency_role.AgencyRole(id='fake')
        gr_mock.side_effect = [
            agency_fake,
            agency_role_fake
        ]
        expected_calls = [
            mock.call(agency.Agency, 'fake_agency'),
            mock.call(
                agency_role.AgencyRole,
                {'agency_id': 'fake',
                 'role_ref_type': 'domain',
                 'role_ref_id': 'fake_domain',
                 'id': 'fake_role'})
        ]
        self._verify(
            'openstack.proxy.Proxy._head',
            self.proxy.check_agency_domain_role,
            method_kwargs={
                'agency': 'fake_agency',
                'domain_id': 'fake_domain',
                'role_id': 'fake_role'
            },
            expected_args=[
                agency_role.AgencyRole,
                agency_role_fake
            ],
        )
        gr_mock.assert_has_calls(expected_calls)

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_grant_agency_domain_role(self, epo_mock, gr_mock):
        agency_fake = agency.Agency(id='fake')
        agency_role_fake = agency_role.AgencyRole(
            id='fake',
            role_ref_type='domain',
            role_ref_id='fake_domain',
            agency_id='fake')
        gr_mock.side_effect = [
            agency_fake,
            agency_role_fake,
        ]
        self._verify(
            'openstack.proxy.Proxy.put',
            self.proxy.grant_agency_domain_role,
            method_kwargs={
                'agency': 'fake_agency',
                'domain_id': 'fake_domain',
                'role_id': 'fake_role'
            },
            expected_args=[
                'v3.0/OS-AGENCY/domains/fake_domain/agencies/fake/roles/fake'
            ],
        )

    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_resource')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_revoke_agency_domain_role(self, epo_mock, gr_mock):
        agency_fake = agency.Agency(id='fake')
        agency_role_fake = agency_role.AgencyRole(
            id='fake',
            role_ref_type='domain',
            role_ref_id='fake_domain',
            agency_id='fake')
        gr_mock.side_effect = [
            agency_fake,
            agency_role_fake,
        ]
        self._verify(
            'openstack.proxy.Proxy._delete',
            self.proxy.revoke_agency_domain_role,
            method_kwargs={
                'agency': 'fake_agency',
                'domain_id': 'fake_domain',
                'role_id': 'fake_role'
            },
            expected_args=[
                agency_role.AgencyRole, agency_role_fake
            ],
        )


class TestIdentitySecurityTokens(TestIdentityProxy):

    @mock.patch('otcextensions.sdk.identity.v3._proxy.Proxy.post')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_create_security_token_token(self, elt_ep_mock, post_mock):
        post_mock.return_value = FakeResponse({
            'credential': {'access': 'f1'}}
        )
        token = self.proxy.create_security_token(duration=2, method='token')
        post_mock.assert_called_with(
            'fake/v3.0/OS-CREDENTIAL/securitytokens',
            json={'auth': {'identity': {
                'methods': ['token'], 'token': {'duration-secods': 2}}}}
        )
        self.assertEqual('f1', token.access)

    @mock.patch('otcextensions.sdk.identity.v3._proxy.Proxy.post')
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_create_security_token_agency(self, elt_ep_mock, post_mock):
        post_mock.return_value = FakeResponse({
            'credential': {'access': 'f1'}}
        )
        token = self.proxy.create_security_token(
            duration=2, method='assume_role',
            domain_id='d1', xrole_name='xr1'
        )
        post_mock.assert_called_with(
            'fake/v3.0/OS-CREDENTIAL/securitytokens',
            json={'auth': {'identity': {
                'methods': ['assume_role'], 'assume_role': {
                    'domain_id': 'd1', 'xrole_name': 'xr1',
                    'duration-secods': 2}}}}
        )
        self.assertEqual('f1', token.access)


class TestIdentityCustomRole(TestIdentityProxy):
    @mock.patch(
        'otcextensions.sdk.identity.v3._proxy.Proxy._get_alternate_endpoint',
        return_value='fake')
    def test_custom_roles(self, epo_mock):
        self.verify_list(
            self.proxy.custom_roles,
            custom_role.CustomRole,
        )
        epo_mock.assert_called_with()
