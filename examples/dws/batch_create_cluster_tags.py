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
Batch create tags for a specified DWS cluster.
"""
import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

cluster_id = 'cluster-uuid'
tags_to_create = [
    {'key': 'key1', 'value': 'value1'},
    {'key': 'key2', 'value': 'value2'}
]

result = conn.dws.batch_create_cluster_tags(cluster_id, tags_to_create)
print(result)
