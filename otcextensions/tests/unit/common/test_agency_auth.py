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

import time

from keystoneauth1 import session
from keystoneauth1.tests.unit import utils

from otcextensions.common import agency_auth


class AgencyTest(utils.TestCase):

    TEST_ROOT_URL = 'http://127.0.0.1:5000/'
    TEST_URL = '%s%s' % (TEST_ROOT_URL, 'v3')
    TEST_ROOT_ADMIN_URL = 'http://127.0.0.1:35357/'
    TEST_ADMIN_URL = '%s%s' % (TEST_ROOT_ADMIN_URL, 'v3')

    TEST_PASS = 'password'

    TEST_APP_CRED_ID = 'appcredid'
    TEST_APP_CRED_SECRET = 'secret'
    TEST_TARGET_DOMAIN_ID = 'agency_domain_id'
    TEST_TARGET_AGENCY_NAME = 'agency_name'
    TEST_TARGET_PROJECT_ID = 'target_project_id'

    def setUp(self):
        super(AgencyTest, self).setUp()
        nextyear = 1 + time.gmtime().tm_year
        self.TEST_RESPONSE_DICT = {
            "token": {
                "methods": [
                    "token",
                    "password"
                ],

                "expires_at": "%i-02-01T00:00:10.000123Z" % nextyear,
                "project": {
                    "domain": {
                        "id": self.TEST_DOMAIN_ID,
                        "name": self.TEST_DOMAIN_NAME
                    },
                    "id": self.TEST_TENANT_ID,
                    "name": self.TEST_TENANT_NAME
                },
                "user": {
                    "domain": {
                        "id": self.TEST_DOMAIN_ID,
                        "name": self.TEST_DOMAIN_NAME
                    },
                    "id": self.TEST_USER,
                    "name": self.TEST_USER
                },
                "issued_at": "2013-05-29T16:55:21.468960Z",
                "catalog": [],  # self.TEST_SERVICE_CATALOG,
                "service_providers": []  # self.TEST_SERVICE_PROVIDERS
            },
        }

    def stub_auth(self, subject_token=None, **kwargs):
        if not subject_token:
            subject_token = self.TEST_TOKEN

        self.stub_url('POST', ['auth', 'tokens'],
                      headers={'X-Subject-Token': subject_token}, **kwargs)

    def test_authenticate_with_username_password(self):
        self.stub_auth(json=self.TEST_RESPONSE_DICT)
        a = agency_auth.Agency(self.TEST_URL,
                               username=self.TEST_USER,
                               password=self.TEST_PASS,
                               target_domain_id=self.TEST_TARGET_DOMAIN_ID,
                               target_agency_name=self.TEST_TARGET_AGENCY_NAME,
                               target_project_id=self.TEST_TARGET_PROJECT_ID)
        self.assertFalse(a.has_scope_parameters)
        s = session.Session(auth=a)

        self.assertEqual({'X-Auth-Token': self.TEST_TOKEN},
                         s.get_auth_headers())

        req = {'auth': {'identity':
               {'methods': ['assume_role'],
                'assume_role': {'domain_id': self.TEST_TARGET_DOMAIN_ID,
                                'xrole_name': self.TEST_TARGET_AGENCY_NAME}},
               'scope': {'project': {'id': self.TEST_TARGET_PROJECT_ID}}}}

        self.assertRequestBodyIs(json=req)
        self.assertRequestHeaderEqual('Content-Type', 'application/json')
        self.assertRequestHeaderEqual('Accept', 'application/json')
        self.assertRequestHeaderEqual('X-Auth-Token', self.TEST_TOKEN)
        self.assertEqual(s.auth.auth_ref.auth_token, self.TEST_TOKEN)
        # TODO(not_gtema): add other tests

    def test_authenticate_with_username_password_roles(self):
        self.stub_auth(json=self.TEST_RESPONSE_DICT)
        a = agency_auth.Agency(self.TEST_URL,
                               username=self.TEST_USER,
                               password=self.TEST_PASS,
                               target_domain_id=self.TEST_TARGET_DOMAIN_ID,
                               target_agency_name=self.TEST_TARGET_AGENCY_NAME,
                               target_project_id=self.TEST_TARGET_PROJECT_ID,
                               roles=["r1", "r2"])
        self.assertFalse(a.has_scope_parameters)
        s = session.Session(auth=a)

        self.assertEqual({'X-Auth-Token': self.TEST_TOKEN},
                         s.get_auth_headers())

        req = {'auth': {'identity':
               {'methods': ['assume_role'],
                'assume_role': {'domain_id': self.TEST_TARGET_DOMAIN_ID,
                                'xrole_name': self.TEST_TARGET_AGENCY_NAME,
                                'restrict': {'roles': ['r1', 'r2']}}},
               'scope': {'project': {'id': self.TEST_TARGET_PROJECT_ID}}}}

        self.assertRequestBodyIs(json=req)
        self.assertRequestHeaderEqual('Content-Type', 'application/json')
        self.assertRequestHeaderEqual('Accept', 'application/json')
        self.assertRequestHeaderEqual('X-Auth-Token', self.TEST_TOKEN)
        self.assertEqual(s.auth.auth_ref.auth_token, self.TEST_TOKEN)
