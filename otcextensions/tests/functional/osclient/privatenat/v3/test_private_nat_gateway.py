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
import uuid

from openstack import connection
from openstack import exceptions as sdk_exceptions
from openstack import resource
from openstackclient.tests.functional import base

from otcextensions import sdk
from otcextensions.tests.functional import base as sdk_base
from otcextensions.tests.functional.privatenat import PrivateNatEnvironmentMixin


class TestPrivateNatGateway(PrivateNatEnvironmentMixin, base.TestCase):
    """Functional tests for private NAT gateway CLI commands."""

    def setUp(self):
        super(TestPrivateNatGateway, self).setUp()
        self.conn = connection.Connection(config=sdk_base.TEST_CLOUD_REGION)
        sdk.register_otc_extensions(self.conn)

    def _create_gateway(self, prefix, description):
        stack = self._create_private_nat_network_stack(prefix)
        self.addCleanup(self._cleanup_private_nat_network_stack, stack)
        gateway_name = "{prefix}-{suffix}".format(
            prefix=prefix, suffix=uuid.uuid4().hex[:8]
        )

        gateway = json.loads(
            self.openstack(
                "privatenat gateway create "
                "--name {name} "
                "--description {description} "
                "--downlink-vpc virsubnet_id={virsubnet_id} "
                "-f json".format(
                    name=gateway_name,
                    description=description,
                    virsubnet_id=stack["subnet"].id,
                )
            )
        )
        self.addCleanup(self._delete_gateway, gateway["id"])
        return {"stack": stack, "gateway": gateway}

    def _delete_gateway(self, gateway_id):
        try:
            gateway = self.conn.natv3.get_private_nat_gateway(gateway_id)
        except sdk_exceptions.ResourceNotFound:
            return

        self.conn.natv3.delete_private_nat_gateway(gateway_id, ignore_missing=True)
        resource.wait_for_delete(self.conn.natv3, gateway, 2, 120)

    def test_private_nat_gateway_list(self):
        json_output = json.loads(self.openstack("privatenat gateway list -f json "))
        self.assertIsNotNone(json_output)

    def test_private_nat_gateway_create(self):
        env = self._create_gateway("cli-private-nat-create", "cli-private-nat-create")
        created = env["gateway"]

        self.assertIsNotNone(created)
        self.assertEqual("cli-private-nat-create", created["description"])

    def test_private_nat_gateway_show(self):
        env = self._create_gateway("cli-private-nat-show", "cli-private-nat-show")
        gateway_id = env["gateway"]["id"]

        shown = json.loads(self.openstack("privatenat gateway show -f json " + gateway_id))
        self.assertEqual(gateway_id, shown["id"])
        self.assertEqual("cli-private-nat-show", shown["description"])

    def test_private_nat_gateway_update(self):
        env = self._create_gateway(
            "cli-private-nat-update", "cli-private-nat-before-update"
        )
        gateway_id = env["gateway"]["id"]

        updated = json.loads(
            self.openstack(
                "privatenat gateway update "
                "--description cli-private-nat-after-update "
                "{gateway_id} -f json".format(gateway_id=gateway_id)
            )
        )
        self.assertEqual(gateway_id, updated["id"])
        self.assertEqual("cli-private-nat-after-update", updated["description"])

        shown = json.loads(self.openstack("privatenat gateway show -f json " + gateway_id))
        self.assertEqual("cli-private-nat-after-update", shown["description"])

    def test_private_nat_gateway_delete(self):
        env = self._create_gateway("cli-private-nat-delete", "cli-private-nat-delete")
        gateway_id = env["gateway"]["id"]
        gateway = self.conn.natv3.get_private_nat_gateway(gateway_id)

        self.openstack("privatenat gateway delete " + gateway_id)
        resource.wait_for_delete(self.conn.natv3, gateway, 2, 120)

        listed = json.loads(self.openstack("privatenat gateway list -f json "))
        self.assertFalse(any(item["Id"] == gateway_id for item in listed))
