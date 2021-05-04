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
List all CBR share members of a CBR backup
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


backup = 'df5d3389-d5ea-4115-b268-53df57c8ed49'
backup = conn.cbr.find_backup(name_or_id=backup)
for member in conn.cbr.members(backup=backup.id):
    print(member)
