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
Get details of CSS Cluster by cluster_id or instance of Cluster class
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

cluster_id = '5ae2d850-c201-4b61-ac06-c2750d0402ba'
resp = conn.css.get_cluster(cluster_id)
print(resp)
