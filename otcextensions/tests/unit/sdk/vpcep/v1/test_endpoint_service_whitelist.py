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
import uuid
from openstack.tests.unit import base

from otcextensions.sdk.vpcep.v1 import endpoint_service


ID = uuid.uuid4().hex
DOMAIN1_ID = 'iam:domain::' + uuid.uuid4().hex
DOMAIN2_ID = 'iam:domain::' + uuid.uuid4().hex


EXAMPLE = {
    "id": ID,
    "permission": "*",
    "created_at": "2018-10-18T13:26:40Z"
}

EXAMPLE_LIST = {
    "permissions":
    [
        DOMAIN1_ID,
        DOMAIN2_ID
    ]
}


class TestEndpointWhitelist(base.TestCase):

    def test_basic(self):
        sot = endpoint_service.Whitelist()
        self.assertEqual('permissions', sot.resources_key)
        path = '/vpc-endpoint-services/%{endpoint_service_id}s/permissions'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint_service.Whitelist(**EXAMPLE)
        for key, value in EXAMPLE.items():
            self.assertEqual(getattr(sot, key), value)


class TestEndpointManageWhitelist(base.TestCase):

    def test_basic(self):
        sot = endpoint_service.ManageWhitelist()
        path = ('/vpc-endpoint-services/%{endpoint_service_id}s'
                '/permissions/action')
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint_service.ManageWhitelist(**EXAMPLE_LIST)
        permissions_list = EXAMPLE_LIST['permissions']
        for i in range(len(permissions_list)):
            self.assertEqual(permissions_list[i], sot.permissions[i])
