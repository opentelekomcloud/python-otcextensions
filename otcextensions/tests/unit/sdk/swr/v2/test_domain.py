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

from otcextensions.sdk.swr.v2 import domain

EXAMPLE = {
    'namespace': 'space',
    'repository': 'repo',
    'access_domain': 'OTC00000000001000000447',
    'permit': 'read',
    'deadline': 'forever',
    'description': 'desc'
}


class TestDomain(base.TestCase):

    def test_basic(self):
        sot = domain.Domain()
        path = 'manage/namespaces/%(namespace)s/' \
               'repositories/%(repository)s/access-domains'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = domain.Domain(**EXAMPLE)
        self.assertEqual(EXAMPLE['access_domain'], sot.access_domain)
        self.assertEqual(EXAMPLE['namespace'], sot.namespace)
        self.assertEqual(EXAMPLE['deadline'], sot.deadline)
        self.assertEqual(EXAMPLE['description'], sot.description)
