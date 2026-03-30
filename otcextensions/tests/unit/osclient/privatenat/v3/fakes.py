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

import mock
from openstackclient.tests.unit import utils

from otcextensions.sdk.natv3.v3 import gateway
from otcextensions.tests.unit.osclient import test_base


def gen_data(data, columns):
    return tuple(getattr(data, attr, "") for attr in columns)


class TestPrivateNat(utils.TestCommand):
    def setUp(self):
        super(TestPrivateNat, self).setUp()

        self.app.client_manager.privatenat = mock.Mock()

        self.client = self.app.client_manager.privatenat


class FakePrivateNatGateway(test_base.Fake):
    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": "name-" + uuid.uuid4().hex,
            "description": "private_nat_gateway_description",
            "spec": "Small",
            "status": "ACTIVE",
            "project_id": "project-" + uuid.uuid4().hex,
            "enterprise_project_id": "ep-" + uuid.uuid4().hex,
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00",
            "rule_max": 20,
            "transit_ip_pool_size_max": 1,
            "downlink_vpcs": [
                {
                    "vpc_id": "vpc-" + uuid.uuid4().hex,
                    "virsubnet_id": "subnet-" + uuid.uuid4().hex,
                    "ngport_ip_address": "192.168.10.10",
                }
            ],
            "tags": [
                {
                    "key": "key1",
                    "value": "value1",
                }
            ],
        }

        obj = gateway.PrivateNatGateway.existing(**object_info)
        return obj
