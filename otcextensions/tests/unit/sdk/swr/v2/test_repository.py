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

from otcextensions.sdk.swr.v2 import repository

EXAMPLE = {
    'namespace': 'org_name',
    'repository': 'repo_name',
    'category': 'windows',
    'description': 'desc',
    'is_public': False,
}


class TestRepository(base.TestCase):

    def test_basic(self):
        sot = repository.Repository()
        path = '/manage/namespaces/%(namespace)s/repos'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = repository.Repository(**EXAMPLE)
        self.assertEqual(EXAMPLE['namespace'], sot.namespace)
        self.assertEqual(EXAMPLE['repository'], sot.repository)
        self.assertEqual(EXAMPLE['category'], sot.category)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['is_public'], sot.is_public)
