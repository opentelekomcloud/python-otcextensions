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

from otcextensions.sdk.mrs.v1 import jobbinary

EXAMPLE = {
    "name": "my-job-binary",
    "url": "/simple/mapreduce/program",
    "is_protected": False,
    "is_public": False,
    "description": "this is the job binary template"
}


class TestJobBinary(base.TestCase):

    def test_basic(self):
        sot = jobbinary.Jobbinary()
        self.assertEqual('job_binary', sot.resource_key)
        self.assertEqual('binaries', sot.resources_key)
        path = '/job-binaries'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_get)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_update)

    def test_make_it(self):
        sot = jobbinary.Jobbinary(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['url'], sot.url)
        self.assertEqual(EXAMPLE['is_public'], sot.is_public)
        self.assertEqual(EXAMPLE['is_protected'], sot.is_protected)
        self.assertEqual(EXAMPLE['description'], sot.description)
