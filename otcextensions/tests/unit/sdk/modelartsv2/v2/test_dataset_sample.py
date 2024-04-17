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
from otcextensions.sdk.modelartsv2.v2 import dataset_sample
from otcextensions.tests.unit.sdk.modelartsv2.v2 import examples
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = examples.DATASET_SAMPLE


class TestDatasetSample(base.TestCase):
    def setUp(self):
        super(TestDatasetSample, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = dataset_sample.DatasetSample()

        self.assertEqual(
            "/datasets/%(dataset_id)s/data-annotations/samples",
            sot.base_path,
        )
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("samples", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

        self.assertDictEqual(
            {
                "email": "email",
                "high_score": "high_score",
                "label_name": "label_name",
                "label_type": "label_type",
                "limit": "limit",
                "locale": "locale",
                "low_score": "low_score",
                "marker": "marker",
                "offset": "offset",
                "order": "order",
                "preview": "preview",
                "process_parameter": "process_parameter",
                "sample_state": "sample_state",
                "sample_type": "sample_type",
                "search_conditions": "search_conditions",
                "version_id": "version_id",
            },
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = dataset_sample.DatasetSample(**EXAMPLE)
        self.assertEqual(sot.id, EXAMPLE["sample_id"])
        for key, value in EXAMPLE.items():
            if key == "metadata":
                pass
            else:
                assert_attributes_equal(self, getattr(sot, key), value)

    def test_delete_samples(self):
        dataset_id = "dataset-id"
        samples = ["sample1-id", "sample2-id"]
        sot = dataset_sample.DatasetSample()
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {"success": True}
        response.headers = {}
        self.sess.post.return_value = response
        rt = sot.delete_samples(self.sess, dataset_id, samples, True)
        json_body = {
            "samples": ["sample1-id", "sample2-id"],
            "delete_source": True,
        }
        url = utils.urljoin(
            sot.base_path % {"dataset_id": dataset_id}, "delete"
        )
        self.sess.post.assert_called_with(url, json=json_body)
        self.assertEqual(rt, sot)
