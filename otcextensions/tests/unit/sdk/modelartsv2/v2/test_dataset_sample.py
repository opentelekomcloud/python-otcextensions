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

EXAMPLE = {
    "annotated_by": "human/OTC-EU-DE-000000000010000XXXXXX/dummy",
    "labels": [{"name": "Tomato_healthy", "property": {}, "type": 0}],
    "metadata": {
        "@modelarts:import_origin": 0,
        "@modelarts:size": [256, 256, 3],
        "@modelarts:source_image_info": "https://dummydummy/test",
    },
    "preview": "https://dummydummy/test",
    "sample_id": "000500f237d4c078ca64f2fd99da9828",
    "sample_status": "MANUAL_ANNOTATION",
    "sample_time": 1694457754000,
    "sample_type": 0,
    "source": "https://dummydummy/testdata",
}


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
        # self.assertEqual('', sot.resource_key)
        self.assertEqual("samples", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        updated_sot_attrs = ["labels", "preview"]
        sot = dataset_sample.DatasetSample(**EXAMPLE)
        # self.assertEqual(EXAMPLE['create_time'], sot.created_at)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_delete_samples(self):
        dataset_id = "dataset-uuid"
        sot = dataset_sample.DatasetSample.existing(dataset_id=dataset_id)
        url = utils.urljoin(sot.base_path, "delete")
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        dataset_samples_ids = [
            "sample1-uuid",
            "sample2-uuid",
        ]
        json_body = {"samples": dataset_samples_ids}
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = None
        response.headers = {}
        self.sess.post.return_value = response

        # When delete_source=False
        rt = sot.delete_samples(
            self.sess,
            dataset_samples_ids,
            delete_source=False,
        )
        self.sess.post.assert_called_with(
            url,
            json=json_body,
            headers=headers,
        )
        self.assertEqual(rt, sot)

        # When delete_source=True
        rt = sot.delete_samples(
            self.sess,
            dataset_samples_ids,
            delete_source=True,
        )
        json_body.update(delete_source=True)
        self.sess.post.assert_called_with(
            url,
            json=json_body,
            headers=headers,
        )
        self.assertEqual(rt, sot)
