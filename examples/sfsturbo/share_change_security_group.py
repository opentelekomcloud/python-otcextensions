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
 Change security group for Sfs Turbo file system
"""
import openstack
from otcextensions import sdk


openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')
sdk.register_otc_extensions(conn)

share = conn.sfsturbo.change_security_group(
    share="2917184a-deeb-4238-8b61-c82e648377d1",
    security_group_id='88a47a36-1b69-41b5-bef8-f74a2a85933f')
print(share)
