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

from otcextensions.sdk.tms.v1 import resource_tag

EXAMPLE = {
    "project_id": "786ef11caa5c43ff80256be4c7fee8b7",
    "resources": [{"resource_id": "2079d0a6-3dbc-4d59-99da-6b8b7c899a97",
                   "resource_type": "vpc"}],
    "tags": [{"key": "ENV1", "value": "dev1"}],
}


class TestResourceTag(base.TestCase):
    def test_basic(self):
        sot = resource_tag.ResourceTag()
        path = "/resource-tags/batch-delete"
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = resource_tag.ResourceTag(**EXAMPLE)
        self.assertEqual(EXAMPLE['tags'], sot.tags)
        self.assertEqual(EXAMPLE['resources'], sot.resources)
        self.assertEqual(EXAMPLE['project_id'], sot.project_id)
