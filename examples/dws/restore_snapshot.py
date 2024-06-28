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
Restore Snapshot to a DWS cluster to a newly created one.
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    'name': 'dws-1',
    'availability_zone': 'eu-de-01',
    'port': 8000,
    'vpc_id': 'router-uuid',
    'subnet_id': 'network-uuid',
    'security_group_id': 'security-group-uuid',
    'public_ip': {
        'public_bind_type': 'auto_assign',
        'eip_id': ''
    }
}

snapshot_id = 'snapshot-uuid'

response = conn.dws.restore_snapshot(snapshot_id, **attrs)
print(response)
