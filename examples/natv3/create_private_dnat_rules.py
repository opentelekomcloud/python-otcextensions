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
Create a Private DNAT Rule
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

dnat_rule_attrs = {
    "gateway_id": "0adefb29-a6c2-48a5-8637-2be67fa03fec",
    "transit_ip_id": "3faa719d-6d18-4ccb-a5c7-33e65a09663e",
    "network_interface_id": "dae9393a-b536-491c-a5a2-72edc1104707",
    "protocol": "tcp",
    "internal_service_port": 22,
    "transit_service_port": 22,
}

dnat_rule = conn.natv3.create_private_dnat_rule(**dnat_rule_attrs)
print(dnat_rule)
