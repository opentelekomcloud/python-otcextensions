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
Create a Group in an existing queue
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    'queue': 'f53aa6a4-424a-4ea4-ab01-9a1b12c1f0a1',  # Required; Queue-ID
    'group': 'g-b9f6941f-ea88-457a-aa50-3efc89e303c0'  # Required; Group-ID
}
raw = conn.dms.delete_group(**attrs)
print(raw)
