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
Get a CCE cluster node by id or class ClusterNode
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


cluster = "cluster_name_or_id"
cluster = conn.cce.find_cluster(cluster)
node_id = "node_id"
node = conn.cce.get_cluster_node(cluster, node_id)
print(node)
