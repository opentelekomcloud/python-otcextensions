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
    # Everything here is required for creation
    'name': 'test-instance-2',
    'engine': 'kafka',
    'engine_version': '2.3.0',
    'storage_space': '600',
    'vpc_id': '26ca2783-dc40-4e3a-95b1-5a0756441e12',
    'security_group_id': '65a3b4b8-b782-4aff-8311-19896597fd4e',
    'subnet_id': 'c6b2dbc9-ca80-4b49-bbbb-85ea9b96f8b3',  # = network_id in GUI
    'available_zones': ['bf84aba586ce4e948da0b97d9a7d62fb'],
    'product_id': '00300-30308-0--0',
    'storage_spec_code': 'dms.physical.storage.ultra'
}
for raw in conn.dms.create_instance(**attrs):
    print(raw)
