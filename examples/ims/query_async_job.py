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
Query Async Job
"""

import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)
attrs = {
    "project_id": "5dd3c0b24cdc4d31952c49589182a89d",
    "job_id": 'ff8080828f9a78db018fe7c6e2f772b2'
}
result = conn.imsv1.get_async_job(**attrs)
print(result)
