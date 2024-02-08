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

from otcextensions.sdk.swr.v2 import organization

EXAMPLE = {
    "namespace": "test_create_org_v2",
    "id": 21,
    "creator_name": "anton",
    "auth": 7,
}

EXAMPLE_PERMISSION = {
    "permissions": [
        {
            "user_id": "5a23ecb3999b458d92d51d524bb7fb4b",
            "user_name": "test",
            "auth": 1
        }
    ],
    "namespace": "test_create_org_v2"
}


class TestOrganization(base.TestCase):

    def test_basic(self):
        sot = organization.Organization()
        self.assertEqual('namespaces', sot.resources_key)
        path = '/manage/namespaces'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = organization.Organization(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['namespace'], sot.namespace)
        self.assertEqual(EXAMPLE['creator_name'], sot.creator_name)
        self.assertEqual(EXAMPLE['auth'], sot.auth)


class TestOrganizationPermissions(base.TestCase):

    def test_basic(self):
        sot = organization.Permission()
        path = '/manage/namespaces/%(namespace)s/access'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = organization.Permission(**EXAMPLE_PERMISSION)
        self.assertEqual(EXAMPLE_PERMISSION['namespace'], sot.namespace)
        self.assertEqual(
            EXAMPLE_PERMISSION['permissions'][0]["user_id"],
            sot.permissions[0].user_id
        )
        self.assertEqual(
            EXAMPLE_PERMISSION['permissions'][0]["auth"],
            sot.permissions[0].auth
        )
        self.assertEqual(
            EXAMPLE_PERMISSION['permissions'][0]["user_name"],
            sot.permissions[0].user_name
        )
