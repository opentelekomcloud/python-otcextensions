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
Create VPC Endpoint
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


sdk.register_otc_extensions(conn)

attrs = {
    "network_id": "894ef6dc-1018-4182-80ce-b30414cbd6dd",
    "router_id": "fc7fbc57-dd83-403f-a325-6a068584f476",
    "tags": [{
        "key": "test1",
        "value": "test1"
    }],
    "endpoint_service_id": "63fa38cf-0ec9-484e-a883-f3c5258ed964",
    "enable_dns": True
}

endpoint = conn.vpcep.create_endpoint(**attrs)
print(endpoint)
