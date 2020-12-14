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
Manage VPC Endpoint Service Whitelist
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

sdk.register_otc_extensions(conn)

endpoint_service_id = '63fa38cf-0ec9-484e-a883-f3c5258ed964'

domains = [
    "iam:domain::5fc973eea581490997e82ea11a1d0101",
    "iam:domain::5fc973eea581490997e82ea11a1d0121",
]
action = "add"

whitelist = conn.vpcep.manage_whitelist(
    endpoint_service_id, domains, action)
for domain_id in whitelist:
    print(domain_id)
print(list(whitelist.permissions))
