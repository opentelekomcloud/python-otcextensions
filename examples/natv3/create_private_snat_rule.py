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
"""
Create a Private SNAT Rule
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

snat_rule_attrs = {
    "gateway_id": "80da6f26-94eb-4537-97f0-5a56f4d04cfb",
    "virsubnet_id": "5b9ea497-727d-4ad0-a99e-3984b3f5aaed",
    "transit_ip_ids": ["36a3049a-1682-48b3-b1cf-cb986a3350ef"],
    "description": "my_snat_rule01",
}

snat_rule = conn.natv3.create_private_snat_rule(**snat_rule_attrs)
print(snat_rule)
