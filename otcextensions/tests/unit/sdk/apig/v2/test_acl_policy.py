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
from otcextensions.sdk.apig.v2 import acl_policy

EXAMPLE_AC_POLICY = {
    'gateway_id': 'gateway-67890',
    'id': 'acl-123',
    'acl_name': 'Test ACL',
    'acl_type': 'IP',
    'acl_value': '192.168.0.1',
    'entity_type': 'APP',
    'update_time': '2025-02-07T13:00:00Z',
    'bind_num': 3,
    'error_code': '',
    'error_msg': ''
}


class TestAcPolicy(base.TestCase):

    def test_basic(self):
        sot = acl_policy.AclPolicy()
        self.assertEqual('apigw/instances/%(gateway_id)s/acls', sot.base_path)
        self.assertEqual('acls', sot.resources_key)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = acl_policy.AclPolicy(**EXAMPLE_AC_POLICY)
        self.assertEqual(EXAMPLE_AC_POLICY['gateway_id'], sot.gateway_id)
        self.assertEqual(EXAMPLE_AC_POLICY['id'], sot.id)
        self.assertEqual(EXAMPLE_AC_POLICY['acl_name'], sot.acl_name)
        self.assertEqual(EXAMPLE_AC_POLICY['acl_type'], sot.acl_type)
        self.assertEqual(EXAMPLE_AC_POLICY['acl_value'], sot.acl_value)
        self.assertEqual(EXAMPLE_AC_POLICY['entity_type'], sot.entity_type)
        self.assertEqual(EXAMPLE_AC_POLICY['update_time'], sot.update_time)
        self.assertEqual(EXAMPLE_AC_POLICY['bind_num'], sot.bind_num)
        self.assertEqual(EXAMPLE_AC_POLICY['error_code'], sot.error_code)
        self.assertEqual(EXAMPLE_AC_POLICY['error_msg'], sot.error_msg)
