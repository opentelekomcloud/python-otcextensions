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
 Add eip to bandwidth
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='test-dmd')

example_bandwidth = conn.vpc.add_eip_to_bandwidth(
    bandwidth="bandwidth-id",
    publicip_info=[{'publicip_id': "publicip-id", 'publicip_type': '5_bgp'}])
print(example_bandwidth)
