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
conn = openstack.connect(cloud="otc")
sdk.register_otc_extensions(conn)

attrs = {
    "name": "test_share_1",
    "share_proto": "NFS",
    "share_type": "STANDARD",
    # For an HPC file system, size must be a multiple of 1.2 TiB (e.g. 3686)
    # and hpc_bw one of "20M", "40M", "125M", "250M", "500M", "1000M".
    "size": 100,
    "availability_zone": "eu-de-01",
    "vpc_id": "vpc_uuid",
    "subnet_id": "subnet_uuid",
    "security_group_id": "security_group_uuid",
    # Optional metadata. crypt_key_id creates an encrypted file system. To
    # deploy an HPC file system set expand_type to "hpc" and provide hpc_bw
    # (size must then be a multiple of 1.2 TiB, e.g. 3686); use "bandwidth"
    # for an enhanced file system.
    "metadata": {"crypt_key_id": "kms_key_uuid"},
}

share = conn.sfsturbo.create_share(**attrs)
conn.sfsturbo.wait_for_share(share)

print(share)
