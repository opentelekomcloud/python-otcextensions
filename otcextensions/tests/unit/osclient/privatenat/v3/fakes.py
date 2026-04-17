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

from otcextensions.sdk.natv3.v3 import dnat
from otcextensions.sdk.natv3.v3 import gateway
from otcextensions.sdk.natv3.v3 import snat
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


class FakePrivateDnatRule(test_base.Fake):
    """Fake one or more Private DNAT Rules"""

    @classmethod
    def generate(cls):
        """Create a fake Private DNAT Rule.

        :return:
            A FakeResource object, with id, status and so on
        """
        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "project_id": "da261828016849188f4dcc2ef94d9da9",
            "description": "test_dnat_rule_description",
            "gateway_id": "private-gw-id-" + uuid.uuid4().hex,
            "transit_ip_id": uuid.uuid4().hex,
            "enterprise_project_id": "ep-" + uuid.uuid4().hex,
            "network_interface_id": "net-" + uuid.uuid4().hex,
            "type": "COMPUTE",
            "protocol": "any",
            "internal_service_port": 0,
            "transit_service_port": 0,
            "private_ip_address": uuid.uuid4().hex,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "status": "ACTIVE",
        }

        obj = dnat.PrivateDnat.existing(**object_info)
        return obj


class FakePrivateSnatRule(test_base.Fake):
    """Fake one or more Private SNAT Rules"""

    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "project_id": "da261828016849188f4dcc2ef94d9da9",
            "description": "test_snat_rule_description",
            "gateway_id": "private-gw-id-" + uuid.uuid4().hex,
            "cidr": "10.0.0.0/24",
            "virsubnet_id": "subnet-" + uuid.uuid4().hex,
            "transit_ip_associations": [
                {
                    "transit_ip_id": "tip-" + uuid.uuid4().hex,
                    "transit_ip_address": "172.20.1.10",
                }
            ],
            "enterprise_project_id": "ep-" + uuid.uuid4().hex,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "status": "ACTIVE",
        }

        obj = snat.PrivateSnat.existing(**object_info)
        return obj
