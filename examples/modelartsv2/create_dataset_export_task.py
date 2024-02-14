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
"""Create a dataset_export_task from attributes."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")
dataset_id = "heZw7Oh7Ha0eiFIzkm8"
attrs = {
    "path": "s3://test-obs-bucket",
    "export_type": 3,
    "export_params": {
        "sample_state": "",
        "export_dest": "DIR",
    },
}

dataset = conn.modelartsv2.create_dataset_export_task(dataset_id, **attrs)
print(dataset)
