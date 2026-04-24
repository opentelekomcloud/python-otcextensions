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
Assign a private transit IP address.
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

transit_ip = conn.natv3.create_private_transit_ip(
    virsubnet_id="2759da7b-8015-404c-ae0a-a389007b0e2a",
    ip_address="192.168.1.68",
    enterprise_project_id="2759da7b-8015-404c-ae0a-a389007b0e2a",
    tags=[{"key": "key1", "value": "value1"}],
)
print(transit_ip)
