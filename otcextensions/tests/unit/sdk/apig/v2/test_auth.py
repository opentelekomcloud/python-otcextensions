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
from openstack.tests.unit import base
from otcextensions.sdk.apig.v2 import api_auth


EXAMPLE_API_AUTH_RESULT = {
    'status': 'AUTHORIZED',
    'error_msg': '',
    'error_code': '',
    'api_name': 'Test API',
    'app_name': 'Test App'
}

EXAMPLE_API_AUTH_INFO = {
    'gateway_id': 'gateway-67890',
    'env_id': 'env-1',
    'app_ids': ['app-12345'],
    'api_ids': ['api-98765'],
    'api_id': 'api-98765',
    'api_name': 'Test API',
    'group_name': 'Group A',
    'api_type': 1,
    'api_remark': 'Test API remark',
    'app_name': 'Test App',
    'app_remark': 'Test App remark',
    'app_type': 'web',
    'app_creator': 'creator-1',
    'publish_id': 'publish-999',
    'group_id': 'group-111',
    'auth_result': EXAMPLE_API_AUTH_RESULT,
    'auth_time': '2025-02-07T12:00:00Z',
    'id': 'auth-abc',
    'app_id': 'app-12345',
    'auth_role': 'admin',
    'auth_tunnel': 'default',
    'auth_whitelist': ['192.168.0.1'],
    'auth_blacklist': ['10.0.0.1'],
    'visit_params': 'param1=value1',
    'visit_param': 'param1',
    'roma_app_type': 'roma-type-1',
    'env_name': 'production',
    'run_env_name': 'prod'
}


class TestApiAuthResult(base.TestCase):

    def test_make_it(self):
        sot = api_auth.ApiAuthResult(**EXAMPLE_API_AUTH_RESULT)
        self.assertEqual(EXAMPLE_API_AUTH_RESULT['status'], sot.status)
        self.assertEqual(EXAMPLE_API_AUTH_RESULT['error_msg'], sot.error_msg)
        self.assertEqual(EXAMPLE_API_AUTH_RESULT['error_code'], sot.error_code)
        self.assertEqual(EXAMPLE_API_AUTH_RESULT['api_name'], sot.api_name)
        self.assertEqual(EXAMPLE_API_AUTH_RESULT['app_name'], sot.app_name)


class TestApiAuthInfo(base.TestCase):

    def test_basic(self):
        sot = api_auth.ApiAuthInfo()
        self.assertEqual('auths', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = api_auth.ApiAuthInfo(**EXAMPLE_API_AUTH_INFO)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['gateway_id'],
                         sot.gateway_id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['env_id'],
                         sot.env_id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['app_ids'],
                         sot.app_ids)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['api_ids'],
                         sot.api_ids)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['api_id'],
                         sot.api_id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['api_name'],
                         sot.api_name)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['group_name'],
                         sot.group_name)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['api_type'],
                         sot.api_type)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['api_remark'],
                         sot.api_remark)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['app_name'],
                         sot.app_name)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['app_remark'],
                         sot.app_remark)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['app_type'],
                         sot.app_type)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['app_creator'],
                         sot.app_creator)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['publish_id'],
                         sot.publish_id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['group_id'],
                         sot.group_id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['auth_time'],
                         sot.auth_time)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['id'], sot.id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['app_id'],
                         sot.app_id)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['auth_role'],
                         sot.auth_role)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['auth_tunnel'],
                         sot.auth_tunnel)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['auth_whitelist'],
                         sot.auth_whitelist)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['auth_blacklist'],
                         sot.auth_blacklist)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['visit_params'],
                         sot.visit_params)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['visit_param'],
                         sot.visit_param)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['roma_app_type'],
                         sot.roma_app_type)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['env_name'],
                         sot.env_name)
        self.assertEqual(EXAMPLE_API_AUTH_INFO['run_env_name'],
                         sot.run_env_name)

        self.assertEqual(EXAMPLE_API_AUTH_RESULT['status'],
                         sot.auth_result.status)
        self.assertEqual(EXAMPLE_API_AUTH_RESULT['api_name'],
                         sot.auth_result.api_name)


class TestApiAuth(base.TestCase):

    def test_basic(self):
        sot = api_auth.ApiAuth()
        self.assertEqual('apis', sot.resources_key)
        self.assertFalse(sot.allow_create)
