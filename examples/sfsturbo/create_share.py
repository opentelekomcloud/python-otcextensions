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
 Create Sfs Turbo file system
"""
import openstack
from otcextensions import sdk


openstack.enable_logging(True)
conn = openstack.connect(cloud='test-terraform')
sdk.register_otc_extensions(conn)

attrs = {
    "name": "test_share_1",
    "share_proto": "NFS",
    "share_type": "STANDARD",
    "size": 100,
    "availability_zone": 'eu-de-01',
    "vpc_id": "019445d1-53fa-4c2f-91be-6d00008bac18",
    "subnet_id": "6d77e947-b846-4b0a-baa0-dad83627012b",
    "security_group_id": "33d26f6c-a807-4952-a68a-554b409063e6"
}

share = conn.sfsturbo.create_share(**attrs)
print(share)
