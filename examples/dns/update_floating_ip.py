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
Update a DNS recordset with new parameters
"""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')


floating_ip = conn.dns.update_floating_ip(
    floating_ip='floating_ip_id',
    ptrdname='update.test.',
    description='My updated Floating IP PTR record',
    ttl=3600
)
print(floating_ip)
