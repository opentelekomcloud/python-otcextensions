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
"""Modifying the Description of a Development Environment Instance."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")
attr = {
    "description": "aha",
}

instance_id = "DE-12c340b2-6434-11ed-98da-0255c0a8005d"
response = conn.modelartsv1.update_devenv_instance(instance_id, **attr)
print(response)
