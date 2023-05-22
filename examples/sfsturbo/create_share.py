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
conn = openstack.connect(cloud='test-terraform-47')
sdk.register_otc_extensions(conn)

attrs = {
    "name": "test_share_1",
    "share_proto": "NFS",
    "share_type": "STANDARD",
    "size": 1,
    "availability_zone": 'eu-de-01',
    "vpc_id": "814b516f-7e4f-4252-9574-0a9de735a508",
    "subnet_id": "151d421d-8dd2-4e34-b37c-3c2627a6bcf9",
    "security_group_id": "cdfde235-5c6b-46b2-80ba-19f87c8cc47d"
}

share = conn.sfsturbo.find_share(name_or_id="sfs-turbo-86e5")
print(share)
