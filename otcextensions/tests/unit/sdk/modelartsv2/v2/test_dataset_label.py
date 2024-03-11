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
import mock
from keystoneauth1 import adapter

from openstack import utils
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv2.v2 import dataset_label
from otcextensions.tests.unit.sdk.modelartsv2.v2 import examples

EXAMPLE = examples.DATASET_LABEL


class TestDatasetLabel(base.TestCase):
    def setUp(self):
        super(TestDatasetLabel, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = dataset_label.DatasetLabel()

        self.assertEqual(
            "/datasets/%(datasetId)s/data-annotations/labels",
            sot.base_path,
        )
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("labels", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)

        self.assertDictEqual(
            {
                "limit": "limit",
                "marker": "marker",
                "version_id": "version_id",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = dataset_label.DatasetLabel(**EXAMPLE)
        self.assertEqual(sot.name, EXAMPLE["name"])
        self.assertEqual(
            sot.property.color, EXAMPLE["property"]["@modelarts:color"]
        )
        self.assertEqual(
            sot.property.default_shape,
            EXAMPLE["property"]["@modelarts:default_shape"],
        )

    def test_update_labels(self):
        dataset_id = "dataset-id"
        labels = [
            {
                "name": "Cat",
                "property": {
                    "@modelarts:color": "#8a1524",
                    "@modelarts:rename_to": "pussycat",
                },
            }
        ]
        sot = dataset_label.DatasetLabel(datasetId=dataset_id)
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {"success": True}
        response.headers = {}
        self.sess.put.return_value = response
        rt = sot.update_labels(self.sess, labels)
        self.sess.put.assert_called_with(
            sot.base_path % {"datasetId": dataset_id}, json={"labels": labels}
        )
        self.assertEqual(rt, sot)

    def test_delete_labels(self):
        dataset_id = "dataset-id"
        labels = [{"name": "Cat"}]
        sot = dataset_label.DatasetLabel(datasetId=dataset_id)
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {"success": True}
        response.headers = {}
        self.sess.post.return_value = response
        rt = sot.delete_labels(self.sess, labels, 2)
        self.sess.post.assert_called_with(
            utils.urljoin(sot.base_path % {"datasetId": dataset_id}, "delete"),
            json={"labels": labels},
            params={"delete_policy": 2},
        )
        self.assertEqual(rt, sot)
