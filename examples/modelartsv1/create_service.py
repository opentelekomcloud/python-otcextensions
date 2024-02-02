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
"""Create a service from attributes."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

attrs = {
  "service_name": "mnist",
  "description": "mnist service",
  "infer_type": "real-time",
  "config": [
    {
      "model_id": "xxxmodel-idxxx",
      "weight": "70",
      "specification": "modelarts.vm.cpu.2u",
      "instance_count": 1,
      "envs":
      {
          "model_name": "mxnet-model-1",
          "load_epoch": "0"
      }
    },
    {
      "model_id": "xxxxxx",
      "weight": "30",
      "specification": "modelarts.vm.cpu.2u",
      "instance_count": 1
    }
  ]
}

service = conn.modelartsv1.create_service(**attrs)
print(service)
