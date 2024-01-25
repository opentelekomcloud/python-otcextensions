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
    "annotated_by": "human/OTC-EU-DE-000000000010000XXXXXX/dummy",
    "labels": [
        {
            "name": "Tomato_healthy",
            "property": {},
            "type": 0,
        },
    ],
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

DELETE_SAMPLES_RESP = {
    "success": False,
    "results": [
        {
            "success": False,
            "error_code": "ModelArts.4420",
            "error_msg": "Sample not found. [sample-id]",
        },
        {
            "success": True,
        },
    ],
}


class TestSample(base.TestCase):
    def setUp(self):
        super(TestSample, self).setUp()

    def test_basic(self):
        sot = dataset.Sample()

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
        updated_sot_attrs = [
            "labels",
        ]
        sot = dataset.Sample(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)


class TestDeleteSample(base.TestCase):
    def setUp(self):
        super(TestDeleteSample, self).setUp()

    def test_basic(self):
        sot = dataset.DeleteSample()

        self.assertEqual(
            "/datasets/%(dataset_id)s/data-annotations/samples/delete",
            sot.base_path,
        )

        self.assertEqual(None, sot.resource_key)
        self.assertEqual(None, sot.resources_key)

        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = dataset.DeleteSample(**DELETE_SAMPLES_RESP)

        for key, value in DELETE_SAMPLES_RESP.items():
            self.assertEqual(getattr(sot, key), value)
