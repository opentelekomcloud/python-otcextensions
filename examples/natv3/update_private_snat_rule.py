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
Update a Private SNAT Rule
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")

snat_rule = conn.natv3.update_private_snat_rule(
    "af4dbb83-7ca0-4ed1-b28b-668c1f9c6b81",
    description="my_snat_rule_update",
    transit_ip_ids=["bbe7c2e7-3bad-445b-a067-b30acce66053"],
)
print(snat_rule)
