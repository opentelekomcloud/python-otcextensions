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
import uuid
from datetime import datetime

import mock

from openstackclient.tests.unit import utils

from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.vpcep.v1 import endpoint_service
from otcextensions.sdk.vpcep.v1 import endpoint


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestVpcep(utils.TestCommand):
    def setUp(self):
        super(TestVpcep, self).setUp()

        self.app.client_manager.vpcep = mock.Mock()

        self.client = self.app.client_manager.vpcep


class FakeEndpointService(test_base.Fake):
    """Fake one or more Nat Gateways."""
    @classmethod
    def generate(cls):
        """Create a fake NAT Gateway.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "port_id": "port-id-" + uuid.uuid4().hex,
            "vpc_id": "vpc-id-" + uuid.uuid4().hex,
            "pool_id": "pool-id-" + uuid.uuid4().hex,
            "status": "available",
            "approval_enabled": False,
            "service_name": "vpcep-service-" + uuid.uuid4().hex,
            "service_type": "interface",
            "server_type": "VM",
            "project_id": "project-id-" + uuid.uuid4().hex,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
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

        return endpoint_service.EndpointService(**object_info)


class FakeEndpoint(test_base.Fake):
    """Fake one or more Endpoint(s)."""
    @classmethod
    def generate(cls):
        """Create a fake SNAT Rule.

        :return:
            A FakeResource object, with id, status and so on
        """
        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "service_type": "interface",
            "marker_id": 322312312312,
            "status": "creating",
            "vpc_id": "vpc-id-" + uuid.uuid4().hex,
            "enable_dns": False,
            "endpoint_service_name": "vpcep-" + uuid.uuid4().hex,
            "endpoint_service_id": "ep-service-id-" + uuid.uuid4().hex,
            "project_id": "project-id-" + uuid.uuid4().hex,
            "whitelist": [
                "127.0.0.1"
            ],
            "enable_whitelist": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "tags": [
                {
                    "key": "test1",
                    "value": "test1"
                }
            ]
        }

        return endpoint.Endpoint(**object_info)
