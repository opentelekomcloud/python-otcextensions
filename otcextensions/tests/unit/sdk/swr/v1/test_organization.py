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
    "organization": "test_create_org_v2",
    "id": 21,
    "creator_name": "anton",
    "auth": 7,
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
        self.assertEqual(EXAMPLE['organization'], sot.organization)
        self.assertEqual(EXAMPLE['creator_name'], sot.creator_name)
        self.assertEqual(EXAMPLE['auth'], sot.auth)
