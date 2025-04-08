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
from otcextensions.sdk.apig.v2 import acl_api_binding


EXAMPLE_ACL_API_BINDING = {
    'gateway_id': 'gateway-67890',
    'id': 'binding-001',
    'api_id': 'api-123',
    'env_id': 'env-1',
    'acl_id': 'acl-456',
    'create_time': '2025-04-01T10:00:00Z'
}

EXAMPLE_ACL_BINDING_FAILURE = {
    'bind_id': 'bind-999',
    'error_code': '403',
    'error_msg': 'Forbidden',
    'api_id': 'api-123',
    'api_name': 'Test API'
}

EXAMPLE_API_FOR_ACL = {
    'gateway_id': 'gateway-67890',
    'api_id': 'api-123',
    'api_name': 'Bound API',
    'api_type': 'REST',
    'api_remark': 'Already bound',
    'env_id': 'env-1',
    'env_name': 'prod',
    'bind_id': 'bind-123',
    'group_name': 'groupA',
    'bind_time': '2025-04-01T09:00:00Z',
    'publish_id': 'pub-321',
    'req_method': 'GET'
}

EXAMPLE_UNBIND_API_FOR_ACL = {
    'gateway_id': 'gateway-67890',
    'id': 'api-999',
    'name': 'Unbound API',
    'group_id': 'group-222',
    'group_name': 'Group B',
    'type': 1,
    'remark': 'Not bound',
    'run_env_name': 'dev',
    'run_env_id': 'env-2',
    'publish_id': 'pub-456',
    'acl_name': 'Test ACL',
    'req_uri': '/test',
    'auth_type': 'NONE',
    'req_method': 'POST'
}

EXAMPLE_ACL_FOR_API = {
    'gateway_id': 'gateway-67890',
    'acl_id': 'acl-456',
    'acl_name': 'Test ACL',
    'entity_type': 'APP',
    'acl_type': 'IP',
    'acl_value': '192.168.1.1',
    'env_id': 'env-1',
    'env_name': 'prod',
    'bind_id': 'bind-001',
    'bind_time': '2025-04-01T08:30:00Z'
}


class TestAclApiBinding(base.TestCase):

    def test_basic(self):
        sot = acl_api_binding.AclApiBinding()
        self.assertEqual('apigw/instances/%(gateway_id)s/acl-bindings',
                         sot.base_path)
        self.assertEqual('acl_bindings', sot.resources_key)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = acl_api_binding.AclApiBinding(**EXAMPLE_ACL_API_BINDING)
        self.assertEqual(EXAMPLE_ACL_API_BINDING['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_ACL_API_BINDING['id'], sot.id)
        self.assertEqual(EXAMPLE_ACL_API_BINDING['api_id'], sot.api_id)
        self.assertEqual(EXAMPLE_ACL_API_BINDING['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_ACL_API_BINDING['acl_id'], sot.acl_id)
        self.assertEqual(EXAMPLE_ACL_API_BINDING['create_time'],
                         sot.create_time)


class TestAclBindingFailure(base.TestCase):

    def test_basic(self):
        sot = acl_api_binding.AclBindingFailure()
        self.assertEqual('failure', sot.resources_key)

    def test_make_it(self):
        sot = acl_api_binding.AclBindingFailure(**EXAMPLE_ACL_BINDING_FAILURE)
        self.assertEqual(EXAMPLE_ACL_BINDING_FAILURE['bind_id'], sot.bind_id)
        self.assertEqual(EXAMPLE_ACL_BINDING_FAILURE['error_code'],
                         sot.error_code)
        self.assertEqual(EXAMPLE_ACL_BINDING_FAILURE['error_msg'],
                         sot.error_msg)
        self.assertEqual(EXAMPLE_ACL_BINDING_FAILURE['api_id'], sot.api_id)
        self.assertEqual(EXAMPLE_ACL_BINDING_FAILURE['api_name'],
                         sot.api_name)


class TestApiForAcl(base.TestCase):

    def test_basic(self):
        sot = acl_api_binding.ApiForAcl()
        self.assertEqual(
            'apigw/instances/%(gateway_id)s/acl-bindings/binded-apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = acl_api_binding.ApiForAcl(**EXAMPLE_API_FOR_ACL)
        self.assertEqual(EXAMPLE_API_FOR_ACL['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_API_FOR_ACL['api_id'], sot.api_id)
        self.assertEqual(EXAMPLE_API_FOR_ACL['api_name'], sot.api_name)
        self.assertEqual(EXAMPLE_API_FOR_ACL['api_type'], sot.api_type)
        self.assertEqual(EXAMPLE_API_FOR_ACL['api_remark'], sot.api_remark)
        self.assertEqual(EXAMPLE_API_FOR_ACL['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_API_FOR_ACL['env_name'], sot.env_name)
        self.assertEqual(EXAMPLE_API_FOR_ACL['bind_id'], sot.bind_id)
        self.assertEqual(EXAMPLE_API_FOR_ACL['group_name'], sot.group_name)
        self.assertEqual(EXAMPLE_API_FOR_ACL['bind_time'], sot.bind_time)
        self.assertEqual(EXAMPLE_API_FOR_ACL['publish_id'], sot.publish_id)
        self.assertEqual(EXAMPLE_API_FOR_ACL['req_method'], sot.req_method)


class TestUnbindApiForAcl(base.TestCase):

    def test_basic(self):
        sot = acl_api_binding.UnbindApiForAcl()
        self.assertEqual(
            'apigw/instances/%(gateway_id)s/acl-bindings/unbinded-apis',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('apis', sot.resources_key)

    def test_make_it(self):
        sot = acl_api_binding.UnbindApiForAcl(**EXAMPLE_UNBIND_API_FOR_ACL)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['gateway_id'],
                         sot.gateway_id)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['id'], sot.id)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['name'], sot.name)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['group_name'],
                         sot.group_name)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['type'], sot.type)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['remark'], sot.remark)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['run_env_name'],
                         sot.run_env_name)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['run_env_id'],
                         sot.run_env_id)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['publish_id'],
                         sot.publish_id)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['acl_name'], sot.acl_name)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['req_uri'], sot.req_uri)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['auth_type'],
                         sot.auth_type)
        self.assertEqual(EXAMPLE_UNBIND_API_FOR_ACL['req_method'],
                         sot.req_method)


class TestAclForApi(base.TestCase):

    def test_basic(self):
        sot = acl_api_binding.AclForApi()
        self.assertEqual(
            'apigw/instances/%(gateway_id)s/acl-bindings/binded-acls',
            sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertEqual('acls', sot.resources_key)

    def test_make_it(self):
        sot = acl_api_binding.AclForApi(**EXAMPLE_ACL_FOR_API)
        self.assertEqual(EXAMPLE_ACL_FOR_API['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_ACL_FOR_API['acl_id'], sot.acl_id)
        self.assertEqual(EXAMPLE_ACL_FOR_API['acl_name'], sot.acl_name)
        self.assertEqual(EXAMPLE_ACL_FOR_API['entity_type'], sot.entity_type)
        self.assertEqual(EXAMPLE_ACL_FOR_API['acl_type'], sot.acl_type)
        self.assertEqual(EXAMPLE_ACL_FOR_API['acl_value'], sot.acl_value)
        self.assertEqual(EXAMPLE_ACL_FOR_API['env_id'], sot.env_id)
        self.assertEqual(EXAMPLE_ACL_FOR_API['env_name'], sot.env_name)
        self.assertEqual(EXAMPLE_ACL_FOR_API['bind_id'], sot.bind_id)
        self.assertEqual(EXAMPLE_ACL_FOR_API['bind_time'], sot.bind_time)
