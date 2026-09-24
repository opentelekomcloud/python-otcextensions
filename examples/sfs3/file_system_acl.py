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
import openstack
from otcextensions import sdk

"""
Configure, read and delete the ACL of an SFS General Purpose File System
(SFS3).

An ACL statement allows a VPC (and optionally a list of source IPs) to
access the file system. ``Action`` is ``FullControl`` (read/write) or
``Read`` (read-only); ``Effect`` is always ``Allow``.
"""

openstack.enable_logging(True)
conn = openstack.connect(cloud="otc")
sdk.register_otc_extensions(conn)

fs_name = "test-sfs3-fs"

# Configure the file system ACL
statements = [
    {
        "Sid": "stmt-1",
        "Action": "FullControl",
        "Effect": "Allow",
        "Condition": {"SourceVpc": "<vpc-id>"},
    }
]
conn.sfs3.create_acl(fs_name, statements)

# Read the file system ACL
acl = conn.sfs3.get_acl(fs_name)
print(acl)

# Delete the file system ACL
conn.sfs3.delete_acl(fs_name)
