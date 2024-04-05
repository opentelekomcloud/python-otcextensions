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
#
"""Manage endpoint service whitelist."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

name_or_id = 'xyz'
action = 'add'
domains = ['domain1-id', 'domain2-id']

endpoint_service = conn.vpcep.find_service(name_or_id)
whitelist = conn.vpcep.service_whitelist(
    endpoint_service, action, domains
)
print(list(whitelist))
