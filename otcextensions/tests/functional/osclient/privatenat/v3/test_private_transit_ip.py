#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import json

from openstackclient.tests.functional import base

from openstack import connection
from openstack import exceptions as sdk_exceptions
from otcextensions import sdk
from otcextensions.tests.functional import base as sdk_base
from otcextensions.tests.functional.privatenat import PrivateNatEnvironmentMixin


class TestPrivateTransitIp(PrivateNatEnvironmentMixin, base.TestCase):
    """Functional Tests for private NAT transit IP addresses"""

    def setUp(self):
        super(TestPrivateTransitIp, self).setUp()
        self.conn = connection.Connection(config=sdk_base.TEST_CLOUD_REGION)
        sdk.register_otc_extensions(self.conn)

    def test_privatenat_transit_ip_list(self):
        json_output = json.loads(self.openstack("privatenat transit ip list -f json "))
        self.assertIsNotNone(json_output)

    def test_privatenat_transit_ip_create(self):
        env = self._prepare_private_nat_subnet_environment(
            "cli-private-transit-ip-create"
        )

        created = json.loads(
            self.openstack(
                "privatenat transit ip create "
                "--virsubnet-id {virsubnet_id} "
                "--tags test=cli "
                "-f json".format(virsubnet_id=env["subnet"].id)
            )
        )
        self.addCleanup(self._delete_private_transit_ip, created["id"])

        self.assertIsNotNone(created)
        self.assertEqual("ACTIVE", created["status"])

    def test_privatenat_transit_ip_show(self):
        env = self._prepare_private_nat_subnet_environment(
            "cli-private-transit-ip-show"
        )

        created = json.loads(
            self.openstack(
                "privatenat transit ip create "
                "--virsubnet-id {virsubnet_id} "
                "-f json".format(virsubnet_id=env["subnet"].id)
            )
        )
        self.addCleanup(self._delete_private_transit_ip, created["id"])

        shown = json.loads(
            self.openstack("privatenat transit ip show -f json " + created["id"])
        )
        self.assertEqual(created["id"], shown["id"])

    def test_privatenat_transit_ip_delete(self):
        env = self._prepare_private_nat_subnet_environment(
            "cli-private-transit-ip-delete"
        )

        created = json.loads(
            self.openstack(
                "privatenat transit ip create "
                "--virsubnet-id {virsubnet_id} "
                "-f json".format(virsubnet_id=env["subnet"].id)
            )
        )

        self.openstack("privatenat transit ip delete " + created["id"])

        with self.assertRaises(sdk_exceptions.ResourceNotFound):
            self.conn.natv3.get_private_transit_ip(created["id"])
