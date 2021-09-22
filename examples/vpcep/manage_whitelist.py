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

endpoint_service_id = 'endpoint-service-uuid'

domains = [
    "iam:domain::domain1-uuid",
    "iam:domain::domain2-uuid"
]
action = "add"

whitelist = conn.vpcep.manage_whitelist(
    endpoint_service_id, domains, action)
print(list(whitelist))
