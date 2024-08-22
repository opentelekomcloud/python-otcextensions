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
Add master and client nodes to CSS Cluster
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect()

cluster_name_or_id = 'a4915eea-7a70-4058-bbf5-c391989c10e3'

attrs = {
    'node_type': 'ess-master',
    'flavor': 'ced8d1a7-eff8-4e30-a3de-cd9578fd518f',
    'node_size': 3,
    'volume_type': 'COMMON',
}

cluster = conn.css.find_cluster(cluster_name_or_id, ignore_missing=False)

conn.css.add_cluster_nodes(cluster, **attrs)
