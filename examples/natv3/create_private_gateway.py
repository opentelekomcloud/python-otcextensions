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
Create a NAT Gateway
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

downlink_vpc = {
    "vpc_id": "3cb66d44-9f75-4237-bfff-e37b14d23ad2",
    "virsubnet_id": "373979ee-f4f0-46c5-80e3-0fbf72646b70",
    "ngport_ip_address": "10.0.0.17",
}
gateway_attrs = {
    "name": "nat_001",
    "description": "my private nat gateway 01",
    "downlink_vpcs": [downlink_vpc],
    "spec": "1",
}

gateway = conn.natv3.create_private_nat_gateway(**gateway_attrs)
print(gateway)
