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
'''
Update MRS Job
'''
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    "name": "my-mapreduce-job-update",
    "mains": [],
    "libs": [
        "2628d0e4-6109-4a09-a338-c4ee1b0963ed"
    ],
    "is_protected": False,
    "interface": [],
    "is_public": False,
    "type": "MapReduce",
    "description": "This is the Map Reduce job template"
}

job = 'job1'
job = conn.mrs.find_job(name_or_id=job)
job = conn.mrs.update_job(job=job, **attrs)
print(job)
