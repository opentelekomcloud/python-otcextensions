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

from otcextensions.sdk.nat.v2 import gateway
from otcextensions.sdk.nat.v2 import snat
from otcextensions.sdk.nat.v2 import dnat


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestNat(utils.TestCommand):
    def setUp(self):
        super(TestNat, self).setUp()

        self.app.client_manager.nat = mock.Mock()

        self.client = self.app.client_manager.nat


class FakeNatGateway(test_base.Fake):
    """Fake one or more datastore versions."""
    @classmethod
    def generate(cls):
        """Create a fake datastore.

        :return:
            A FakeResource object, with id, name, metadata, and so on
        """
        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "name": "name-" + uuid.uuid4().hex,
            "router_id": "router-" + uuid.uuid4().hex,
            "status": "PENDING_CREATE",
            "description": "my nat gateway",
            "admin_state_up": 'true',
            "tenant_id": "tenant-id-" + uuid.uuid4().hex,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%s")[:-4],
            "spec": "1",
            "internal_network_id": "net-id-" + uuid.uuid4().hex
        }

        return gateway.Gateway(**object_info)

    @staticmethod
    def find_gateway(nat_gateway, name_or_id):
        """Get a Mock object with faked dnat_rule.
        :param dnat_rule:
            A FakeResource objects faking dnat_rule
        :return:
            A Mock object with side_effect set to a faked
            dnat_rule
        """
        if name_or_id in [nat_gateway.id, nat_gateway.name]:
            return mock.Mock(return_value=nat_gateway)
        else:
            return mock.Mock(side_effect=RuntimeError('404 Not Found'))


class FakeSnatRule(test_base.Fake):
    """Fake one or more Instance."""
    @classmethod
    def generate(cls):
        """Create a fake Configuration.

        :return:
            A FakeResource object, with id, name, metadata, and so on
        """

        # Set default attributes.
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "floating_ip_id": "eip-id-" + uuid.uuid4().hex,
            "status": "PENDING_CREATE",
            "nat_gateway_id": "gw-id-" + uuid.uuid4().hex,
            "admin_state_up": True,
            "network_id": "net-id-" + uuid.uuid4().hex,
            "cidr": uuid.uuid4().hex,
            "source_type": 0,
            "tenant_id": "tenant-id-" + uuid.uuid4().hex,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%s")[:-4],
            "floating_ip_address": uuid.uuid4().hex
        }

        return snat.Snat.existing(**object_info)

    @staticmethod
    def get_snat_rule(snat_rule, snat_rule_id):
        """Get a Mock object with faked dnat_rule.
        :param dnat_rule:
            A FakeResource objects faking dnat_rule
        :return:
            A Mock object with side_effect set to a faked
            dnat_rule
        """
        if snat_rule.id == snat_rule_id:
            return mock.Mock(return_value=snat_rule)
        else:
            return mock.Mock(side_effect=RuntimeError('404 Not Found'))


class FakeDnatRule(test_base.Fake):
    """Fake one or more Backup"""
    @classmethod
    def generate(cls):
        object_info = {
            "id": "id-" + uuid.uuid4().hex,
            "floating_ip_id": "eip-id-" + uuid.uuid4().hex,
            "status": "ACTIVE",
            "nat_gateway_id": "gw-id-" + uuid.uuid4().hex,
            "admin_state_up": True,
            "private_ip": uuid.uuid4().hex,
            "internal_service_port": 0,
            "protocol": "any",
            "tenant_id": "abc",
            "port_id": "",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%s")[:-4],
            "floating_ip_address": uuid.uuid4().hex,
            "external_service_port": 0
        }

        obj = dnat.Dnat.existing(**object_info)
        return obj

    @staticmethod
    def get_dnat_rule(dnat_rule, dnat_rule_id):
        """Get a Mock object with faked dnat_rule.
        :param dnat_rule:
            A FakeResource objects faking dnat_rule
        :return:
            A Mock object with side_effect set to a faked
            dnat_rule
        """
        if dnat_rule.id == dnat_rule_id:
            return mock.Mock(return_value=dnat_rule)
        else:
            return mock.Mock(side_effect=RuntimeError('404 Not Found'))
