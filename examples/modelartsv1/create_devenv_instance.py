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
    "name": "notebook-d115",
    "flavor": "modelarts.vm.cpu.2u",
    "spec": {
        "storage": {
            "location": {"path": "/test-bucket/notebooks/"},
            "type": "obs",
        }
    },
    "profile_id": "Multi-Engine 1.0 (python3)-cpu",
}

devenv_instance = conn.modelartsv1.create_devenv_instance(**attrs)
print(devenv_instance)
