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
Create an Instance
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    'name': 'test-instance-2',
    'engine': 'kafka',
    'engine_version': '2.3.0',
    'storage_space': '600',
    'vpc_id': 'vpc_id',
    'security_group_id': 'sec_group_id',
    'subnet_id': 'network_id',
    'available_zones': ['az_id'],
    'product_id': 'product_id',
    'storage_spec_code': 'dms.physical.storage.ultra'
}
for raw in conn.dms.create_instance(**attrs):
    print(raw)
