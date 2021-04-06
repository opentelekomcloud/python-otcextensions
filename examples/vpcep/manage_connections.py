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
conn = openstack.connect(cloud='qainfra')

sdk.register_otc_extensions(conn)

args = {
    "endpoints": [
        "f5ed95ed-2eeb-4e85-a21f-945a9c72e2eb"
    ],
    "action": "receive"
}

endpoint_service_id = 'c92dc513-befd-463d-b225-bfdb8b53a7d9'
connections = conn.vpcep.manage_connections(
    endpoint_service_id, **args)
for connection in connections:
    print(connection)
