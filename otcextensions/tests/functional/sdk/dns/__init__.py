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
        cidr = '192.168.0.0/16'
        ipv4 = 4
        uuid_v4 = uuid.uuid4().hex[:8]
        router_name = 'sdk-dns-test-add-router-' + uuid_v4
        net_name = 'sdk-dns-test-add-net-' + uuid_v4
        subnet_name = 'sdk-dns-test-add-subnet-' + uuid_v4

        network = self.conn.network.create_network(name=net_name)
        self.assertEqual(net_name, network.name)
        net_id = network.id
        subnet = self.conn.network.create_subnet(
            name=subnet_name,
            ip_version=ipv4,
            network_id=net_id,
            cidr=cidr
        )
        self.assertEqual(subnet_name, subnet.name)
        subnet_id = subnet.id

        router = self.conn.network.create_router(name=router_name)
        self.assertEqual(router_name, router.name)
        router_id = router.id
        interface = router.add_interface(
            self.conn.network,
            subnet_id=subnet_id
        )
        self.assertEqual(interface['subnet_id'], subnet_id)
        self.assertIn('port_id', interface)
        return {
            'router_id': router_id,
            'subnet_id': subnet_id,
            'network_id': net_id
        }

    def destroy_network(self, params: dict):
        router_id = params.get('router_id')
        subnet_id = params.get('subnet_id')
        network_id = params.get('network_id')
        router = self.conn.network.get_router(router_id)

        interface = router.remove_interface(
            self.conn.network,
            subnet_id=subnet_id
        )
        self.assertEqual(interface['subnet_id'], subnet_id)
        self.assertIn('port_id', interface)
        sot = self.conn.network.delete_router(
            router_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_subnet(
            subnet_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
        sot = self.conn.network.delete_network(
            network_id,
            ignore_missing=False
        )
        self.assertIsNone(sot)
