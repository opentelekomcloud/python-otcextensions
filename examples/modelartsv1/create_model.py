#!/usr/bin/env python3
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
"""Create a model from attributes."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

attrs = {
    "model_name": "mnist",
    "model_version": "1.0.0",
    "source_location": "https://models.obs.xxxx.com/mnist",
    "source_job_id": "55",
    "source_job_version": "V100",
    "model_type": "TensorFlow",
    "runtime": "python2.7",
    "description": "mnist model",
    "execution_code": "https://testmodel.obs.xxxx.com/customize_service.py",
    "input_params": [
        {
            "url": "/v1/xxx/image",
            "protocol": "http",
            "method": "post",
            "param_name": "image_url",
            "param_type": "string",
            "min": 0,
            "max": 9,
            "param_desc": "http://test/test.jpeg",
        }
    ],
    "output_params": [
        {
            "url": "/v1/xxx/image",
            "protocol": "http",
            "method": "post",
            "param_name": "face_location",
            "param_type": "box",
            "param_desc": "face_location param value description",
        }
    ],
    "dependencies": [
        {
            "installer": "pip",
            "packages": [
                {
                    "package_name": "numpy",
                    "package_version": "1.5.0",
                    "restraint": "ATLEAST",
                }
            ],
        }
    ],
    "model_algorithm": "object_detection",
    "model_metrics": '{"f1":0.52381,"recall":0.666667,"precision":0.466667,"accuracy":0.625}',
    "apis": [
        {
            "url": "/v1/xxx/image",
            "protocol": "http",
            "method": "post",
            "input_params": {
                "type": "object",
                "properties": {"image_url": {"type": "string"}},
            },
            "output_params": {
                "type": "object",
                "properties": {"face_location": {"type": "box"}},
            },
        }
    ],
}

model = conn.modelartsv1.create_model(**attrs)
print(model)
