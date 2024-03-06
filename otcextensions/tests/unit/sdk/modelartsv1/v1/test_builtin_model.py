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
from otcextensions.sdk.modelartsv1.v1 import builtin_model


EXAMPLE = {
    "model_id": 4,
    "model_name": "ResNet_v2_50",
    "model_usage": 1,
    "model_precision": "75.55%(top1), 92.6%(top5)",
    "model_size": 102503801,
    "model_train_dataset": "ImageNet, 1,000 classes for image classification",
    "model_dataset_format": "shape: [H>=32, W>=32, C>=1]; type: int8",
    "model_description_url": "https://github.com/....../resnet.py",
    "parameter": [
        {
            "label": "batch_size",
            "value": "4",
            "required": True,
        }
    ],
    "create_time": 1522218780025,
    "engine_id": 501,
    "engine_name": "MXNet",
    "engine_version": "MXNet-1.2.1-python2.7",
}


class TestBuiltInModel(base.TestCase):
    def setUp(self):
        super(TestBuiltInModel, self).setUp()

    def test_basic(self):
        sot = builtin_model.BuiltInModel()

        self.assertEqual("/built-in-algorithms", sot.base_path)
        self.assertEqual("models", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)

    def test_make_it(self):
        sot = builtin_model.BuiltInModel(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key == "create_time":
                self.assertEqual(EXAMPLE[key], sot.created_at)
            elif key == "parameter":
                self.assertEqual(
                    EXAMPLE[key][0]["label"], sot.parameter[0].label
                )
                self.assertEqual(
                    EXAMPLE[key][0]["required"], sot.parameter[0].required
                )
                self.assertEqual(
                    EXAMPLE[key][0]["value"], sot.parameter[0].value
                )
            else:
                self.assertEqual(getattr(sot, key), value)
