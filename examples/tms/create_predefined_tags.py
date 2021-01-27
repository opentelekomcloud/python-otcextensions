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
conn = openstack.connect(cloud='otc')

attrs = {
    "name": "nat_001",
    "description": "my nat gateway 01",
    "router_id": "d84f345c-80a1-4fa2-a39c-d0d397c3f09a",
    "internal_network_id": "89d66639-aacb-4929-969d-07080b0f9fd9",
    "spec": "1"
}

gateway = conn.nat.create_gateway(**attrs)
print(gateway)
