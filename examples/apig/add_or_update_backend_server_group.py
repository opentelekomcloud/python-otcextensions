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
Add or update backend server group
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    "member_groups": [{
        "member_group_name": "vpc_member_group",
        "member_group_weight": 10
    }]
}
result = conn.apig.add_or_update_backend_server_group(
    gateway="gateway_id",
    vpc_channel="vpc_channel_id",
    **attrs
)
