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
Restore a Distributed Cache Service instance.
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


instance = 'instance_id'
backup_id = 'backup_id'
restore = conn.dcs.restore_instance(
    instance=instance,
    backup_id=backup_id,
    description='Test restore of DCS instance'
)
print(restore)
