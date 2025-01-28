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

from otcextensions.sdk.function_graph.v2 import dependency

EXAMPLE = {
    "id": "4f4ae4eb-dcdc-4dd3-bffd-79600bd972b3",
    "owner": "*****",
    "link": "https://{bucket}.{obs_endpoint}.zip",
    "runtime": "Python3.6",
    "etag": "83863be4b6c3a86aef995dbc83aae68f",
    "size": 577118,
    "name": "python-kafka",
    "description": "Python library for Kafka operations.",
    "file_name": "python-kafka.zip",
    "version": 0,
    "dep_id": "edbd67fa-f107-40b3-af75-a85f0577ad61",
    "last_modified": 1660029887
}


class TestFunctionDependency(base.TestCase):

    def test_basic(self):
        sot = dependency.Dependency()
        path = '/fgs/dependencies'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = dependency.Dependency(**EXAMPLE)
        self.assertEqual(EXAMPLE['file_name'], sot.file_name)
        self.assertEqual(EXAMPLE['link'], sot.link)
