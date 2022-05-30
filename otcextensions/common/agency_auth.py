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
import json

from keystoneauth1 import _utils as utils
from keystoneauth1 import access
from keystoneauth1 import exceptions
from keystoneauth1 import loading
from keystoneauth1.identity.v3 import base


_logger = utils.get_logger(__name__)


class AssumeRoleMethod(base.AuthMethod):
    _method_parameters = ['user_id',
                          'username',
                          'user_domain_id',
                          'user_domain_name',
                          'password',
                          'roles',
                          'target_agency_name',
                          'target_domain_id',
                          'target_domain_name',
                          'target_project_id',
                          'target_project_name']

    def get_auth_data(self, session, auth, headers, **kwargs):
        user = {'password': self.password}

        if self.user_id:
            user['id'] = self.user_id
        elif self.username:
            user['name'] = self.username

            if self.user_domain_id:
                user['domain'] = {'id': self.user_domain_id}
            elif self.user_domain_name:
                user['domain'] = {'name': self.user_domain_name}

        return 'password', {'user': user}

    def get_assume_role_auth_data(self, session, auth, headers, **kwargs):
        agency = {'xrole_name': self.target_agency_name}

        if self.target_domain_id:
            agency['domain_id'] = self.target_domain_id
        elif self.target_domain_name:
            agency['domain_name'] = self.target_domain_name
        if self.roles:
            agency['restrict'] = {'roles': list(self.roles)}

        return 'assume_role', agency

    def get_cache_id_elements(self):
        return dict(('assume_role_%s' % p, getattr(self, p))
                    for p in self._method_parameters)


class Agency(base.AuthConstructor):
    """A plugin for authenticating with a username and password.
    It then does assume_role
    """
    _auth_method_class = AssumeRoleMethod

    def __init__(self, auth_url,
                 *args,
                 **kwargs):
        super(Agency, self).__init__(auth_url=auth_url,
                                     *args,
                                     **kwargs)
        self.target_project_id = kwargs.get('target_project_id')
        self.target_project_name = kwargs.get('target_project_name')
        self.target_domain_id = kwargs.get('target_domain_id')
        self.target_domain_name = kwargs.get('target_domain_name')

    def get_auth_ref(self, session, **kwargs):
        # First do regular authorization
        auth_access = super(Agency, self).get_auth_ref(session, **kwargs)
        # And now reauth with another scope
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token': auth_access._auth_token
        }
        body = {'auth': {'identity': {}}}
        ident = body['auth']['identity']
        rkwargs = {}

        for method in self.auth_methods:
            name, auth_data = method.get_assume_role_auth_data(
                session, self, headers, request_kwargs=rkwargs)
            # NOTE(adriant): Methods like ReceiptMethod don't
            # want anything added to the request data, so they
            # explicitly return None, which we check for.
            if name:
                ident.setdefault('methods', []).append(name)
                ident[name] = auth_data

        if not ident:
            raise exceptions.AuthorizationFailure(
                'Authentication method required (e.g. password)')

        if self.target_project_id:
            body['auth']['scope'] = {'project': {'id': self.target_project_id}}
        elif self.target_project_name:
            scope = body['auth']['scope'] = {'project': {}}
            scope['project']['name'] = self.target_project_name
        # If project is not set - get a domain scope
        elif self.target_domain_id:
            body['auth']['scope'] = {'domain':
                                     {'id': self.target_domain_id}}
        elif self.target_domain_name:
            body['auth']['scope'] = {'domain':
                                     {'name': self.target_domain_name}}

        token_url = self.token_url

        if not self.auth_url.rstrip('/').endswith('v3'):
            token_url = '%s/v3/auth/tokens' % self.auth_url.rstrip('/')

        if not self.include_catalog:
            token_url += '?nocatalog'

        _logger.debug('Making authentication request to %s', token_url)
        resp = session.post(token_url, json=body, headers=headers,
                            authenticated=False, log=False, **rkwargs)

        try:
            _logger.debug(json.dumps(resp.json()))
            resp_data = resp.json()
        except ValueError:
            raise exceptions.InvalidResponse(response=resp)

        if 'token' not in resp_data:
            raise exceptions.InvalidResponse(response=resp)

        return access.AccessInfoV3(auth_token=resp.headers['X-Subject-Token'],
                                   body=resp_data)


class AgencyLoader(loading.BaseV3Loader):
    @property
    def plugin_class(self):
        return Agency

    def get_options(self, **kwargs):
        options = super(AgencyLoader, self).get_options()
        options.extend([
            loading.Opt('user-id', help='User ID'),
            loading.Opt('username', help='Username',
                        deprecated=[loading.Opt('user-name')]),
            loading.Opt('user-domain-id', help="User's domain id"),
            loading.Opt('user-domain-name', help="User's domain name"),
            loading.Opt('password', secret=True, prompt='Password: ',
                        help="User's password"),

            loading.Opt('target-agency-name', help="Agency name"),
            loading.Opt('target-project-id',
                        help="Project id available through agency"),
            loading.Opt('target-project-name',
                        help="Project name available through agency"),
            loading.Opt('target-domain-id',
                        help="Domain id available through agency"),
            loading.Opt('target-domain-name',
                        help="Domain name available through agency"),
            loading.Opt('roles',
                        help="List of the roles to request from agency"),
        ])
        return options

    def load_from_options(self, **kwargs):
        if (
            kwargs.get('username')
            and not (kwargs.get('user_domain_name')
                     or kwargs.get('user_domain_id'))
        ):
            m = "You have provided a username. In the V3 identity API a " \
                "username is only unique within a domain so you must " \
                "also provide either a user_domain_id or user_domain_name."
            raise exceptions.OptionError(m)
        if (
            not kwargs.get('target_agency_name')
            or not (kwargs.get('target_domain_id')
                    or kwargs.get('target_domain_name'))
        ):
            m = "Using agency based authorization requires " \
                "target_agency_name, target_domain_id or "\
                "target_domain_name at the very minimum"
            raise exceptions.OptionError(m)

        return super(AgencyLoader, self).load_from_options(**kwargs)
