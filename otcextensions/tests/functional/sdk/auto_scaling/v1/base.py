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

import os
import uuid

import fixtures

from openstack import exceptions
from openstack import _log
from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class BaseASTest(base.BaseFunctionalTest):

    UUID = uuid.uuid4().hex[:9]
    NETWORK_NAME = "test-as-network-" + UUID
    SUBNET_NAME = "test-as-subnet-" + UUID
    ROUTER_NAME = "test-as-router-" + UUID
    KP_NAME = "test-as-kp-" + UUID
    IP_VERSION = 4
    CIDR = "192.168.0.0/16"

    def _create_keypair(self):
        return self.conn.compute.create_keypair(
            name=self.KP_NAME
        )

    def _delete_keypair(self, key_pair):
        return self.conn.compute.delete_keypair(
            keypair=key_pair
        )

    def _create_network(self):
        return self.conn.network.create_network(
            name=self.NETWORK_NAME
        )

    def _delete_network(self, network):
        return self.conn.network.delete_network(
            network=network
        )

    def _create_subnet(self, network_id):
        return self.conn.network.create_subnet(
            name=self.SUBNET_NAME,
            network_id=network_id,
            ip_version=self.IP_VERSION,
            cidr=self.CIDR
        )

    def _delete_subnet(self, subnet):
        return self.conn.network.delete_subnet(
            subnet=subnet
        )

    def _create_router(self, subnet_id):
        router = self.conn.network.create_router(
            name=self.ROUTER_NAME
        )
        self.conn.network.add_interface_to_router(
            router=router,
            subnet_id=subnet_id
        )
        return router

    def _delete_router(self, router, subnet_id):
        self.conn.network.remove_interface_from_router(
            router=router,
            subnet_id=subnet_id
        )
        return self.conn.network.delete_router(
            router=router
        )

    def create_test_infra(self):
        key_pair = self._create_keypair()
        network = self._create_network()
        subnet = self._create_subnet(network.id)
        router = self._create_router(subnet.id)
        return {
            "key_pair_id": key_pair.id,
            "network_id": network.id,
            "subnet_id": subnet.id,
            "router_id": router.id
        }

    def delete_test_infra(self, infra: dict):
        router = self.conn.network.get_router(infra.get("router_id"))
        subnet = self.conn.network.get_subnet(infra.get("subnet_id"))
        network = self.conn.network.get_network(infra.get("network_id"))
        key_pair = self.conn.compute.get_keypair(infra.get("key_pair_id"))
        if router:
            self._delete_router(router, subnet.id)
        if subnet:
            self._delete_subnet(subnet)
        if network:
            self._delete_network(network)
        if key_pair:
            self._delete_keypair(key_pair)

    def setUp(self):
        test_timeout = 3 * int(os.environ.get('OS_TEST_TIMEOUT'))
        try:
            self.useFixture(
                fixtures.EnvironmentVariable(
                    'OS_TEST_TIMEOUT', str(test_timeout)))
        except ValueError:
            pass
        super(BaseASTest, self).setUp()
        self.infra = self.create_test_infra()

    def tearDown(self):
        try:
            self.delete_test_infra(self.infra)
        except exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        super(BaseASTest, self).tearDown()
