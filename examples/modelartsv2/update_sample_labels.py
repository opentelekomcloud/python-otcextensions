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
"""Update sample labels."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

dataset_id = "QWgyNuIgMcSvpUlc6Cu"
attrs = {
    "samples": [
        {
            "sample_id": "8b583c44bf249f8ba43ea42c92920221",
            "labels": [{"name": "yunbao"}],
        },
        {
            "sample_id": "b5fe3039879660a2e6bf18166e247f68",
            "labels": [{"name": "yunbao"}],
        },
    ]
}
response = conn.modelartsv2.update_dataset_labels(dataset_id, **attrs)
print(response)
