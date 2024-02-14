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
"""Create a devenv instance from attributes."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")
attrs = {
    "workspace_id": "0",
    "dataset_name": "dataset-test",
    "dataset_type": 0,
    "data_sources": [
        {
            "data_type": 0,
            "data_path": "/modelarts-data-test/dataset/input/",
        }
    ],
    "description": "",
    "work_path": "/modelarts-data-test/dataset/output/",
    "work_path_type": 0,
    "ai_project": "",
}

dataset = conn.modelartsv2.create_dataset(**attrs)
print(dataset)
