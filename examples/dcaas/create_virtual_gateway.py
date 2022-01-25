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
 Create virtual gateway
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='devstack-admin')
sdk.register_otc_extensions(conn)

attrs = {
    "vpc_id": "24f86468-b729-493c-b122-f430e15e646e",
    "local_ep_group_id": "30f8c88d-5a12-4a32-ab67-93710dda88e1"
}

vg = conn.dcaas.create_virtual_gateway(**attrs)
print(vg)
