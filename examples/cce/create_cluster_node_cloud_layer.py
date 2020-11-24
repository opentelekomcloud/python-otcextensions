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
Create CCE Cluster node
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


node = conn.create_cce_cluster_node(
    availability_zone='eu-de-02',
    cluster='7ca53d10-2a70-11eb-9ade-0255ac1017a0',
    count=1,
    flavor='s2.large.2',
    keypair='tischrei-pub',
    name='tinosnode',
    root_volume_size=40,
    root_volume_type='SATA',
    wait=False)
print(node)
