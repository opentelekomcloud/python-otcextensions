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
Find a single MRS Job binary by name or id
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

name_or_id = 'name_or_id'
job_binary = conn.mrs.find_jobbinary(name_or_id)
print(job_binary)
