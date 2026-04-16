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

import openstack
from openstack import exceptions as sdk_exceptions
from openstack import resource

from otcextensions.tests.functional import base
from otcextensions.tests.functional.privatenat import PrivateNatEnvironmentMixin

_logger = openstack._log.setup_logging("openstack")


class TestGateway(PrivateNatEnvironmentMixin, base.BaseFunctionalTest):
    TEST_PREFIX = "sdk-private-nat-"

    def setUp(self):
        super(TestGateway, self).setUp()
        self._cleanup_stale_private_nat_test_resources()

    def _cleanup_stale_private_nat_test_resources(self):
        for gateway in self.conn.natv3.private_nat_gateways():
            if not gateway.name or not gateway.name.startswith(self.TEST_PREFIX):
                continue
            self._delete_private_nat_gateway(gateway)

        self.cleanup_stale_routers(self.TEST_PREFIX)

        for vpc in self.conn.vpc.vpcs():
            if not vpc.name or not vpc.name.startswith(self.TEST_PREFIX):
                continue
            subnets = list(self.conn.vpc.subnets(vpc_id=vpc.id))
            for subnet in subnets:
                self.conn.vpc.delete_subnet(subnet, ignore_missing=True)
                resource.wait_for_delete(self.conn.vpc, subnet, 2, 120)
            self.conn.vpc.delete_vpc(vpc, ignore_missing=True)
            resource.wait_for_delete(self.conn.vpc, vpc, 2, 120)

    def test_private_nat_gateway_list(self):
        gateways = list(self.conn.natv3.private_nat_gateways())
        self.assertGreaterEqual(len(gateways), 0)

    def test_create_private_nat_gateway(self):
        env = self._prepare_private_nat_gateway_environment("sdk-private-nat-create")
        gateway = env["gateway"]

        fetched = self.conn.natv3.get_private_nat_gateway(gateway.id)
        self.assertEqual(gateway.id, fetched.id)
        self.assertEqual(env["stack"]["subnet"].id, fetched.downlink_vpcs[0].virsubnet_id)

    def test_get_private_nat_gateway(self):
        env = self._prepare_private_nat_gateway_environment("sdk-private-nat-get")
        gateway = self.conn.natv3.get_private_nat_gateway(env["gateway"].id)

        self.assertEqual(env["gateway"].id, gateway.id)
        self.assertEqual(env["stack"]["subnet"].id, gateway.downlink_vpcs[0].virsubnet_id)

    def test_update_private_nat_gateway(self):
        env = self._prepare_private_nat_gateway_environment("sdk-private-nat-update")
        gateway = self.conn.natv3.update_private_nat_gateway(
            env["gateway"], description="sdk-private-nat-updated"
        )

        self.assertEqual("sdk-private-nat-updated", gateway.description)

        fetched = self.conn.natv3.get_private_nat_gateway(env["gateway"].id)
        self.assertEqual("sdk-private-nat-updated", fetched.description)

    def test_delete_private_nat_gateway(self):
        env = self._prepare_private_nat_gateway_environment("sdk-private-nat-delete")
        gateway = env["gateway"]

        fetched = self.conn.natv3.get_private_nat_gateway(gateway.id)
        self.assertEqual(gateway.id, fetched.id)

        self.conn.natv3.delete_private_nat_gateway(gateway, ignore_missing=False)
        resource.wait_for_delete(self.conn.natv3, gateway, 2, 120)

        with self.assertRaises(sdk_exceptions.ResourceNotFound):
            self.conn.natv3.get_private_nat_gateway(gateway.id)
