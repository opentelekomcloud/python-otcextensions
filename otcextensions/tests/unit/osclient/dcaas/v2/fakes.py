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

from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.dcaas.v2 import connection
from otcextensions.sdk.dcaas.v2 import endpoint_group


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestDcaas(utils.TestCommand):
    def setUp(self):
        super(TestDcaas, self).setUp()
        self.app.client_manager.dcaas = mock.Mock()
        self.client = self.app.client_manager.dcaas


class FakeDirectConnection(test_base.Fake):
    """Fake one or more Direct Connection"""
    @classmethod
    def generate(cls):
        """Create a fake Direct Connection.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": "name-" + uuid.uuid4().hex,
            "port_type": "1G",
            "bandwidth": 10,
            "provider": "OTC",
            "location": "Biere",
            "description": 'test description',
            "peer_location": 'test_peer_loc',
            "device_id": '172.16.40.2',
            "interface_name": 'Eth-Trunk2',
            "redundant_id": '11111',
            "provider_status": 'ACTIVE',
            "type": 'hosted',
            "hosting_id": 'test_11',
            "vlan": 11,
            "charge_mode": 'traffic',
            "order_id": 'id1',
            "product_id": 'idp1',
            "status": 'ACTIVE',
            "admin_state_up": True
        }
        return connection.Connection(**object_info)


class FakeEndpointGroup(test_base.Fake):
    """Fake one or more Endpoint Group"""
    @classmethod
    def generate(cls):
        """Create a fake Endpoint Group.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": "name" + uuid.uuid4().hex,
            "description": "test description",
            "endpoints": ["10.2.0.0/24", "10.3.0.0/24"],
            "tenant_id": "tid" + uuid.uuid4().hex,
            "type": "cidr"
        }
        return endpoint_group.DirectConnectEndpointGroup(**object_info)
