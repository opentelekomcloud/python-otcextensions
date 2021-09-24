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
Restart CSS Cluster by cluster_id or instance of Cluster class
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

cluster_id = 'cluter-uuid'
conn.css.restart_cluster(cluster_id)
