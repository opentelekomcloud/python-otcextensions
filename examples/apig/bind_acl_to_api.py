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
Bind Access Control Policy to API
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
attrs = {
    "acl_id": "d5645ed3c454492f8d6aa68ab034c6d3",
    "publish_ids": ["293fe0a8e3f04a1ab151bd0d913900a9"]
}
result = list(conn.apig.bind_acl_to_api(gateway='gateway_id', **attrs))
