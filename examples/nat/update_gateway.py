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
Update a NAT Gateway by gateway_id or instance of Gateway class
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    "name": "new_name",
    "description": "new description",
    "spec": "1"
}

name_or_id = 'gateway_name_or_id'
gateway = conn.nat.find_gateway(name_or_id, ignore_missing=False)
response = conn.nat.update_gateway(gateway, **attrs)
print(response)
