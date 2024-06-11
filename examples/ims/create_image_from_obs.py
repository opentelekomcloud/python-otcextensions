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
Create Image
"""

import openstack
from otcextensions import sdk

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)
attrs = {
    "name": "CentOS-7-x86_64-GenericCloud.qcow2",
    "description": "Create an image from a file in an OBS bucket",
    "image_url": "imsv2-extensions-test:CentOS-7-x86_64.qcow2",
    "os_version": "CentOS 7.0 64bit",
    "min_disk": 40,
    "image_tags": [{"key": "key2", "value": "value2"},
                   {"key": "key1", "value": "value1"}]
}
result = conn.imsv2.create_image(**attrs)
print(result)
