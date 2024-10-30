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
from urllib.parse import urlparse

from openstack.utils import urljoin

from openstack.identity.v3 import _proxy

from otcextensions.sdk.identity.v3 import agency as _agency
from otcextensions.sdk.identity.v3 import agency_role as _agency_role
from otcextensions.sdk.identity.v3 import credential as _credential
from otcextensions.sdk.identity.v3 import security_token as _security_token
from otcextensions.sdk.identity.v3 import custom_role as _custom


class Proxy(_proxy.Proxy):

    def __init__(self, session, *args, **kwargs):
        super(Proxy, self).__init__(session=session, *args, **kwargs)
        self._credentials_base = None

    def _get_alternate_endpoint(self):
        if not self._credentials_base:
            identity_url = self.get_endpoint_data().url
            parsed_domain = urlparse(identity_url)
            self._credentials_base = '%s://%s' % (parsed_domain.scheme,
                                                  parsed_domain.netloc)
        return self._credentials_base

    # ========== Credentials ==========
    def credentials(self, **attrs):
        """Retrieve a generator of credentials

        :param dict query: Optional query parameters to be sent to limit the
            resources being returned.
            * `user_id`: user_id

        :returns: A generator of credentials
            :class:`~otcextensions.sdk.identity.v3.credential.Credential`
            instances
        """
        # for list we need to pass corrected endpoint
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _credential.Credential.base_path)
        return self._list(_credential.Credential, base_path=base_path,
                          **attrs)

    def create_credential(self, **attrs):
        """Create a new credential from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.identity.v3.credential.Credential`,
            comprised of the properties on the Credential class.
        :returns: The results of credential creation
        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._create(_credential.Credential, prepend_key=True,
                            **attrs)

    def get_credential(self, credential):
        """Get a credential

        :param credential: The value can be the ID of a credential
            or a :class:`~otcextensions.sdk.identity.v3.credential.Credential`
            instance.
        :returns: Credential instance
        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._get(_credential.Credential, credential)

    def find_credential(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single credential

        :param name_or_id: The name or ID of a credential
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the credential does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent credential.

        :returns: ``None``
        """
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _credential.Credential.base_path)
        return self._find(_credential.Credential, name_or_id,
                          ignore_missing=ignore_missing,
                          base_path=base_path,
                          **attrs)

    def delete_credential(self, credential, ignore_missing=True):
        """Delete a credential

        :param credential: The value can be the ID of a credential
            or a :class:`~otcextensions.sdk.identity.v3.credential.Credential`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the credential does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent credential.

        :returns: Credential been deleted
        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._delete(_credential.Credential,
                            credential,
                            ignore_missing=ignore_missing)

    def update_credential(self, credential, **attrs):
        """Update credential attributes

        :param credential: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.identity.v3.credential.Credential`

        :rtype: :class:`~otcextensions.sdk.identity.v3.credential.Credential`
        """
        return self._update(_credential.Credential, credential, **attrs)

    # ========== Agencies ==========
    def _agency_normalize_domain_id(self, **attrs):
        if 'domain_id' not in attrs:
            # User missed passing domain_id. Let's assume he wants to list own
            # agencies.
            # Otherwise he should have passed domain_id=None
            access = self.session.auth.get_auth_ref(self)
            if access.domain_id:
                attrs['domain_id'] = access.domain_id
            elif access.project_domain_id:
                attrs['domain_id'] = access.project_domain_id
            elif access.user_domain_id:
                attrs['domain_id'] = access.user_domain_id
        elif attrs['domain_id'] is None:
            # even though requests will eject this prop, do not rely on this
            # functionality
            attrs.pop('domain_id')
        return attrs

    def agencies(self, **attrs):
        """Retrieve a generator of agencies

        When domain_id query parameter is not set - current domain_id will be
        used. Passing domain_id=None allow removing filtering.

        :param dict attrs: Optional query parameters to be sent to limit the
            resources being returned.
            * `domain_id`: Current domain ID
            * `name`: Name of the agency
            * `trust_domain_id`: ID of the delegated domain.

        :returns: A generator of agencies
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
            instances
        """
        # for list we need to pass corrected endpoint
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _agency.Agency.base_path)
        attrs = self._agency_normalize_domain_id(**attrs)

        return self._list(_agency.Agency, base_path=base_path,
                          **attrs)

    def create_agency(self, **attrs):
        """Create a new agency from attributes

        :param dict attrs: Keyword arguments which will be used to create
            a :class:`~otcextensions.sdk.identity.v3.agency.Agency`,
            comprised of the properties on the Agency class.
        :returns: The results of agency creation
        :rtype: :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        """
        attrs = self._agency_normalize_domain_id(**attrs)
        return self._create(_agency.Agency, prepend_key=True,
                            **attrs)

    def get_agency(self, agency):
        """Get a agency

        :param agency: The value can be the ID of a agency
            or a :class:`~otcextensions.sdk.identity.v3.agency.Agency`
            instance.
        :returns: Agency instance
        :rtype: :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        """
        return self._get(_agency.Agency, agency)

    def find_agency(self, name_or_id, ignore_missing=True, **attrs):
        """Find a single agency

        :param name_or_id: The name or ID of a agency
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the agency does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent agency.

        :returns: ``None``
        """
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _agency.Agency.base_path)
        attrs = self._agency_normalize_domain_id(**attrs)
        return self._find(_agency.Agency, name_or_id,
                          ignore_missing=ignore_missing,
                          base_path=base_path,
                          **attrs)

    def delete_agency(self, agency, ignore_missing=True):
        """Delete a agency

        :param agency: The value can be the ID of a agency
            or a :class:`~otcextensions.sdk.identity.v3.agency.Agency`
            instance.
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the agency does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent agency.

        :returns: Agency been deleted
        :rtype: :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        """
        return self._delete(_agency.Agency,
                            agency,
                            ignore_missing=ignore_missing)

    def update_agency(self, agency, **attrs):
        """Update agency attributes

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param dict attrs: attributes for update on
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`

        :rtype: :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        """
        return self._update(_agency.Agency, agency, **attrs)

    # ========== Agency roles ==========

    def agency_project_roles(self, agency, project_id):
        """Retrieve a generator of agency roles on a project

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param project_id: ID of a project

        :returns: A generator of agencies
            :class:`~otcextensions.sdk.identity.v3.agency_role.AgencyRole`
            instances
        """
        # for list we need to pass corrected endpoint
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _agency_role.AgencyRole.base_path)
        agency = self._get_resource(_agency.Agency, agency)

        return self._list(_agency_role.AgencyRole,
                          base_path=base_path,
                          role_ref_type='project',
                          role_ref_id=project_id,
                          agency_id=agency.id)

    def check_agency_project_role(self, agency, project_id, role_id):
        """Check whether role is granted on the project through agency

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param project_id: ID of a project
        :param role_id: ID of a role to check

        :returns:
            :class:`~otcextensions.sdk.identity.v3.agency_role.AgencyRole`
         """
        agency = self._get_resource(_agency.Agency, agency)
        agency_role = self._get_resource(
            _agency_role.AgencyRole,
            {
                'agency_id': agency.id,
                'role_ref_type': 'project',
                'role_ref_id': project_id,
                'id': role_id
            }
        )
        return self._head(_agency_role.AgencyRole,
                          agency_role)

    def grant_agency_project_role(self, agency, project_id, role_id):
        """Grant permission of agency on a project

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param project_id: ID of a project
        :param role_id: ID of a role to revoke

        :returns:
         """
        agency = self._get_resource(_agency.Agency, agency)
        agency_role = self._get_resource(
            _agency_role.AgencyRole,
            {
                'agency_id': agency.id,
                'role_ref_type': 'project',
                'role_ref_id': project_id,
                'id': role_id
            }
        )
        req = agency_role._prepare_request()
        self.put(req.url)

    def revoke_agency_project_role(self, agency, project_id, role_id):
        """Revoke permission of agency on a project

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param project_id: ID of a project
        :param role_id: ID of a role to revoke

        :returns:
         """
        agency = self._get_resource(_agency.Agency, agency)
        agency_role = self._get_resource(
            _agency_role.AgencyRole,
            {
                'agency_id': agency.id,
                'role_ref_type': 'project',
                'role_ref_id': project_id,
                'id': role_id
            }
        )
        return self._delete(_agency_role.AgencyRole, agency_role)

    def agency_domain_roles(self, agency, domain_id):
        """Retrieve a generator of agency roles on a domain

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param domain_id: ID of a domain

        :returns: A generator of agencies
            :class:`~otcextensions.sdk.identity.v3.agency_role.AgencyRole`
            instances
        """
        # for list we need to pass corrected endpoint
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _agency_role.AgencyRole.base_path)
        agency = self._get_resource(_agency.Agency, agency)

        return self._list(_agency_role.AgencyRole,
                          base_path=base_path,
                          role_ref_type='domain',
                          role_ref_id=domain_id,
                          agency_id=agency.id)

    def check_agency_domain_role(self, agency, domain_id, role_id):
        """Check whether role is granted on the domain through agency

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param domain_id: ID of a domain
        :param role_id: ID of a role to check

        :returns:
            :class:`~otcextensions.sdk.identity.v3.agency_role.AgencyRole`
         """
        agency = self._get_resource(_agency.Agency, agency)
        agency_role = self._get_resource(
            _agency_role.AgencyRole,
            {
                'agency_id': agency.id,
                'role_ref_type': 'domain',
                'role_ref_id': domain_id,
                'id': role_id
            }
        )
        return self._head(_agency_role.AgencyRole,
                          agency_role)

    def grant_agency_domain_role(self, agency, domain_id, role_id):
        """Grant permission of agency on a domain

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param domain_id: ID of a domain
        :param role_id: ID of a role to revoke

        :returns:
         """
        agency = self._get_resource(_agency.Agency, agency)
        agency_role = self._get_resource(
            _agency_role.AgencyRole,
            {
                'agency_id': agency.id,
                'role_ref_type': 'domain',
                'role_ref_id': domain_id,
                'id': role_id
            }
        )
        req = agency_role._prepare_request()
        self.put(req.url)

    def revoke_agency_domain_role(self, agency, domain_id, role_id):
        """Revoke permission of agency on a domain

        :param agency: The id or an instance of
            :class:`~otcextensions.sdk.identity.v3.agency.Agency`
        :param domain_id: ID of a domain
        :param role_id: ID of a role to revoke

        :returns:
         """
        agency = self._get_resource(_agency.Agency, agency)
        agency_role = self._get_resource(
            _agency_role.AgencyRole,
            {
                'agency_id': agency.id,
                'role_ref_type': 'domain',
                'role_ref_id': domain_id,
                'id': role_id
            }
        )
        return self._delete(_agency_role.AgencyRole, agency_role)

    # ========== Security Token (temp AK/SK) ==========

    def create_security_token(self, duration, method='token', **attrs):
        """Create a new temporary AK/SK

        :param int duration: Duration in seconds for the token validity.
        :param str method: Authorization method (token or agency)
        :param dict attrs: Keyword arguments which will be used to create a
            :class:`~otcextensions.sdk.identity.v3.security_token.SecurityToken`,
            comprised of the properties on the SecurityToken class.
        :returns: The results of temporary security token creation
        :rtype:
            :class:`~otcextensions.sdk.identity.v3.security_token.SecurityToken`
        """
        # This method is so unique (similar to getting initial auth), that we
        # need to do this totally differently
        body = {
            'auth': {
                'identity': {
                    'methods': [method],
                    method: {**attrs}
                },
            }
        }
        body['auth']['identity'][method]['duration-secods'] = duration
        uri = '%s/v3.0/OS-CREDENTIAL/securitytokens' % (
            self._get_alternate_endpoint()
        )
        response = self.post(uri, json=body)
        token = _security_token.SecurityToken()
        token._translate_response(response)
        return token

    def custom_roles(self, **attrs):
        """Retrieve a generator of custom roles

        :param dict attrs: Optional query parameters to be sent to limit the
            resources being returned.
            * `page`: Page number for pagination query.
            * `per_page`: Number of data records to be displayed on each page.

        :returns: A generator of custom roles
            :class:`~otcextensions.sdk.identity.v3._custom.CustomRole`
            instances
        """
        # for list, we need to pass corrected endpoint
        base = self._get_alternate_endpoint()
        base_path = urljoin(base, _custom.CustomRole.base_path)

        return self._list(_custom.CustomRole, base_path=base_path,
                          **attrs)
