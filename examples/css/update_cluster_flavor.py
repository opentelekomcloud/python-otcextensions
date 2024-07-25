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
Modify CSS Cluster specifications
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect()

cluster_name_or_id = 'asomogyi_0506_updated'

new_flavor = 'd9dc06ae-b9c4-4ef4-acd8-953ef4205e27'

cluster = conn.css.find_cluster(cluster_name_or_id)

conn.css.update_cluster_flavor(cluster, new_flavor, check_replica=False)
