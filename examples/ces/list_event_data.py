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
List all CloudEye event data
"""
import openstack


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


query = {
    'namespace': 'SYS.ECS',
    'type': 'instance_host_info',
    'dim.0': 'instance_id,6e83e6e7-3bf4-4b5b-b390-e80447ef1234', # key, value
    'from': '1596067200', # unix timestamp in ms
    'to': '1597929178' # unix timestamp in ms
}


for data in conn.ces.event_data(**query):
    print(data)
