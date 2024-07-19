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
Update CSS Cluster kernel
"""

import openstack

openstack.enable_logging(True)
conn = openstack.connect()

cluster_name_or_id = 'csstest0716'
cluster = conn.css.find_cluster(cluster_name_or_id)

upgrade_type = 'cross'
target_image = conn.css.get_cluster_version_upgrade_info(cluster, upgrade_type)
target_image = next(iter(target_image.image_info_list))
if target_image:
    target_image_id = target_image.id
    indices_backup_check = True
    agency = 'css_upgrade_agency'
    cluster_load_check = True
    conn.css.update_cluster_kernel(
        cluster,
        target_image_id,
        upgrade_type,
        indices_backup_check,
        agency,
        cluster_load_check,
    )
