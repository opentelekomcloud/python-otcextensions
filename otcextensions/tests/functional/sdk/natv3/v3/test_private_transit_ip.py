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
from otcextensions.tests.functional import base
from otcextensions.tests.functional.privatenat import PrivateNatEnvironmentMixin

_logger = openstack._log.setup_logging("openstack")


class TestPrivateTransitIp(PrivateNatEnvironmentMixin, base.BaseFunctionalTest):
    def test_list_transit_ips(self):
        transit_ips = list(self.conn.natv3.private_transit_ips())
        self.assertGreaterEqual(len(transit_ips), 0)

    def test_get_private_transit_ip(self):
        env = self._prepare_private_nat_subnet_environment("sdk-private-transit-ip-get")

        created = self.conn.natv3.create_private_transit_ip(
            virsubnet_id=env["subnet"].id
        )
        self.addCleanup(self._delete_private_transit_ip, created.id)

        transit_ip = self.conn.natv3.get_private_transit_ip(created.id)
        self.assertEqual(created.id, transit_ip.id)

    def test_create_private_transit_ip(self):
        env = self._prepare_private_nat_subnet_environment(
            "sdk-private-transit-ip-create"
        )

        transit_ip = self.conn.natv3.create_private_transit_ip(
            virsubnet_id=env["subnet"].id,
            tags=[{"key": "test", "value": "sdk"}],
        )
        self.addCleanup(self._delete_private_transit_ip, transit_ip.id)

        self.assertIsNotNone(transit_ip.id)
        self.assertEqual("ACTIVE", transit_ip.status)

    def test_delete_private_transit_ip(self):
        env = self._prepare_private_nat_subnet_environment(
            "sdk-private-transit-ip-delete"
        )

        transit_ip = self.conn.natv3.create_private_transit_ip(
            virsubnet_id=env["subnet"].id
        )

        self.conn.natv3.delete_private_transit_ip(transit_ip, ignore_missing=False)

        with self.assertRaises(sdk_exceptions.ResourceNotFound):
            self.conn.natv3.get_private_transit_ip(transit_ip.id)
