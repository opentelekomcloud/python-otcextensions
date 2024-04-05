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
"""Create VPC Endpoint Service."""
import openstack

openstack.enable_logging(True)
conn = openstack.connect(cloud='otc')

attrs = {
    'port_id': 'port-id',
    'vpc_id': 'router-id',
    'service_name': 'test-service',
    'approval_enabled': False,
    'service_type': 'interface',
    'server_type': 'VM',
    'ports': [{'client_port': 8080, 'server_port': 90, 'protocol': 'TCP'}],
}

endpoint_service = conn.vpcep.create_service(**attrs)
print(endpoint_service)
