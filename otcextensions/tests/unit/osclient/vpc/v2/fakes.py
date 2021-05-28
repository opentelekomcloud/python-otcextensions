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
from datetime import datetime

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.vpc.v2 import peering
from otcextensions.sdk.vpc.v2 import route


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestVpc(utils.TestCommand):
    def setUp(self):
        super(TestVpc, self).setUp()

        self.app.client_manager.vpc = mock.Mock()

        self.client = self.app.client_manager.vpc


class FakeVpcPeering(test_base.Fake):
    """Fake one or more VPC peering connections."""
    @classmethod
    def generate(cls):
        """Create a fake VPC peering connection.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": "name-" + uuid.uuid4().hex,
            "request_vpc_info": {
                "vpc_id": uuid.uuid4().hex,
                "tenant_id": uuid.uuid4().hex
            },
            "accept_vpc_info": {
                "vpc_id": uuid.uuid4().hex,
                "tenant_id": uuid.uuid4().hex
            },
            "status": "ACTIVE",
            "description": "my vpc peering",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        }

        return peering.Peering(**object_info)


class FakeVpcRoute(test_base.Fake):
    """Fake one or more VPC routes."""
    @classmethod
    def generate(cls):
        """Create a fake VPC route.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "type": "peering",
            "nexthop": uuid.uuid4().hex,
            "router_id": uuid.uuid4().hex,
            "project_id": uuid.uuid4().hex,
            "destination": "192.168.200.0/24",
        }

        return route.Route(**object_info)
