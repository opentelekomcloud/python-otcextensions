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
#
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv2.v2 import dataset

EXAMPLE = {
  "import_type" : "dir",
  "import_path" : "s3://test-obs/daoLu_images/cat-rabbit/",
  "included_tags" : [ ],
  "import_annotations" : False,
  "difficult_only" : False
}


class TestDatasetImportTask(base.TestCase):
    def setUp(self):
        super(TestDatasetImportTask, self).setUp()

    def test_basic(self):
        sot = dataset.DatasetImportTask()

        self.assertEqual("/datasets/%(dataset_id)s/import-tasks", sot.base_path)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("import_tasks", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = []
        sot = dataset.DatasetImportTask(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
