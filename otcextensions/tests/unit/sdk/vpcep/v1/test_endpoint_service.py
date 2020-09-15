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
import uuid
from openstack.tests.unit import base

from otcextensions.sdk.vpcep.v1 import endpoint_service


ID = uuid.uuid4().hex
PORT_ID = uuid.uuid4().hex
VPC_ID = uuid.uuid4().hex
POOL_ID = uuid.uuid4().hex
PROJECT_ID = uuid.uuid4().hex

EXAMPLE = {
    "id": ID,
    "port_id": PORT_ID,
    "vpc_id": VPC_ID,
    "pool_id": POOL_ID,
    "status": "available",
    "approval_enabled": False,
    "service_name": "test123",
    "service_type": "interface",
    "server_type": "VM",
    "project_id": PROJECT_ID,
    "created_at": "2018-01-30T07:42:01.174",
    "ports":
    [
        {
            "client_port": 8080,
            "server_port": 90,
            "protocol": "TCP"
        },
        {
            "client_port": 8081,
            "server_port": 80,
            "protocol": "TCP"
        }
    ]
}


class TestEndpointService(base.TestCase):

    def test_basic(self):
        sot = endpoint_service.EndpointService()
        self.assertEqual('endpoint_services', sot.resources_key)
        path = '/vpc-endpoint-services'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = endpoint_service.EndpointService(**EXAMPLE)
        for key in EXAMPLE.keys():
            if key == 'ports':
                ports_list = EXAMPLE[key]
                for i in range(len(ports_list)):
                    for sub_key in ports_list[i].keys():
                        self.assertEqual(ports_list[i][sub_key],
                                         getattr(sot.ports[i], sub_key))
            else:
                self.assertEqual(EXAMPLE[key], getattr(sot, key))
