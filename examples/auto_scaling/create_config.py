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
Create Auto-Scaling Configuration.
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    'name': 'test-config',
    'instance_config': {
        'flavorRef': 's2.medium.1',
        'imageRef': '1616e0b6-503a-4698-946f-cf9942c4c73b',
        'disk': [{
            'size': 20,
            'volume_type': 'SATA',
            'disk_type': 'SYS'
        }],
        'key_name': 'test-key',
    }
}

config = conn.auto_scaling.create_config(**attrs)
print(config)
