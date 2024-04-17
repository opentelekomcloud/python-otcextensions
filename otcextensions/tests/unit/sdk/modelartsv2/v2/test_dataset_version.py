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
from otcextensions.sdk.modelartsv2.v2 import dataset_version
from otcextensions.tests.unit.sdk.modelartsv2.v2 import examples
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = examples.DATASET_VERSION

EXAMPLE_CREATE = {
    "version_name": "V004",
    "version_format": "Default",
    "description": "",
    "clear_hard_property": True,
}


class TestDataset(base.TestCase):
    def setUp(self):
        super(TestDataset, self).setUp()

    def test_basic(self):
        sot = dataset_version.DatasetVersion()

        self.assertEqual("/datasets/%(dataset_id)s/versions", sot.base_path)
        self.assertEqual("versions", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

        self.assertDictEqual(
            {
                "limit": "limit",
                "marker": "marker",
                "status": "status",
                "train_evaluate_ratio": "train_evaluate_ratio",
                "version_format": "version_format",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = dataset_version.DatasetVersion(**EXAMPLE)
        self.assertEqual(sot.id, EXAMPLE["version_id"])
        for key, value in EXAMPLE.items():
            if key == "create_time":
                self.assertEqual(sot.created_at, EXAMPLE[key])
            elif key == "label_stats":
                for ix, data in enumerate(value):
                    self.assertEqual(sot.label_stats[ix].name, data["name"])
                    self.assertEqual(sot.label_stats[ix].type, data["type"])
                    self.assertEqual(sot.label_stats[ix].count, data["count"])
                    self.assertEqual(
                        sot.label_stats[ix].sample_count, data["sample_count"]
                    )
                    self.assertEqual(
                        sot.label_stats[ix].attributes, data["attributes"]
                    )
                    self.assertEqual(
                        sot.label_stats[ix].property.color,
                        data["property"]["@modelarts:color"],
                    )
                    self.assertEqual(
                        sot.label_stats[ix].property.shortcut,
                        data["property"]["@modelarts:shortcut"],
                    )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)

    def test_create_sot(self):
        sot = dataset_version.DatasetVersion(**EXAMPLE_CREATE)
        assert_attributes_equal(self, sot, EXAMPLE_CREATE)
