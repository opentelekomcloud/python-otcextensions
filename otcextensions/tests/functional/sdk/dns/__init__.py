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

from otcextensions.tests.functional import base


class TestDns(base.BaseFunctionalTest):
    uuid_v4 = uuid.uuid4().hex[:8]
    router_name = 'sdk-test-router-' + uuid_v4
    net_name = 'sdk-test-net-' + uuid_v4
    subnet_name = 'sdk-test-subnet-' + uuid_v4
    router_id = None
    net_id = None
    subnet_id = None

    def setUp(self):
        super(TestDns, self).setUp()
        test_timeout = 3 * int(os.environ.get('OS_TEST_TIMEOUT'))
        try:
            self.useFixture(
                fixtures.EnvironmentVariable(
                    'OS_TEST_TIMEOUT', str(test_timeout)))
        except ValueError:
            pass
        self.client = self.conn.dns

    def create_network(self):
        self.cidr = '192.168.0.0/16'
        self.ipv4 = 4

        network = self.conn.network.create_network(name=self.net_name)
        self.assertEqual(self.net_name, network.name)
        self.net_id = network.id
        subnet = self.conn.network.create_subnet(
            name=self.subnet_name,
            ip_version=self.ipv4,
            network_id=self.net_id,
            cidr=self.cidr
        )
        self.assertEqual(self.subnet_name, subnet.name)
        self.subnet_id = subnet.id

        router = self.conn.network.create_router(name=self.router_name)
        self.assertEqual(self.router_name, router.name)
        self.router_id = router.id
        interface = router.add_interface(
            self.conn.network,
            subnet_id=self.subnet_id
        )
        self.assertEqual(interface['subnet_id'], self.subnet_id)
        self.assertIn('port_id', interface)

    def destroy_network(self):
        router = self.conn.network.get_router(self.router_id)

        interface = router.remove_interface(
            self.conn.network,
            subnet_id=self.subnet_id
        )
        self.assertEqual(interface['subnet_id'], self.subnet_id)
        self.assertIn('port_id', interface)
        sot = self.conn.network.delete_router(
            self.router_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_subnet(
            self.subnet_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_network(
            self.net_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
