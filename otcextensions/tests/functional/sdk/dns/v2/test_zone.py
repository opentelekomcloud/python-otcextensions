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
import uuid

import openstack
from otcextensions.tests.functional.sdk.dns import TestDns

_logger = openstack._log.setup_logging("openstack")


class TestZone(TestDns):
    def setUp(self):
        super(TestZone, self).setUp()
        self._cleanup_stale_routers()
        self.zone = None
        self.networks = []

        unique = uuid.uuid4().hex[:8]
        self.public_zone_alias = f"{unique}dns.sdk-test-zone-public.com."
        self.private_zone_alias = f"{unique}dns.sdk-test-zone-private.com."

    def tearDown(self):
        if self.zone:
            try:
                self.client.delete_zone(self.zone)
                self.client.wait_for_delete_zone(self.zone)
            except openstack.exceptions.ResourceNotFound:
                pass
            except openstack.exceptions.SDKException as e:
                _logger.warning(
                    "Got exception during clearing zone resource: %s",
                    str(e),
                )

        for network in self.networks:
            try:
                self.destroy_network(network)
            except openstack.exceptions.SDKException as e:
                _logger.warning(
                    "Got exception during clearing network resource: %s",
                    str(e),
                )

        super(TestZone, self).tearDown()

    def _cleanup_routers(self):
        """Clean up router resources if they are not deleted for any reason."""
        for router in self.conn.network.routers():
            if router.name and router.name.startswith("sdk-dns-test-add-router-"):
                try:
                    ports = list(self.conn.network.ports(device_id=router.id))
                    for port in ports:
                        fixed_ips = getattr(port, "fixed_ips", []) or []
                        for fixed_ip in fixed_ips:
                            subnet_id = fixed_ip.get("subnet_id")
                            if subnet_id:
                                try:
                                    self.conn.network.remove_interface_from_router(
                                        router, subnet_id=subnet_id
                                    )
                                except openstack.exceptions.SDKException:
                                    pass

                    self.conn.network.delete_router(router, ignore_missing=True)
                except openstack.exceptions.SDKException as e:
                    _logger.warning(
                        "Failed to cleanup stale router %s: %s",
                        router.id,
                        str(e),
                    )

    def _create_zone(self, zone_name, router_id=None, zone_type="public"):
        attrs = {"name": zone_name}

        if zone_type != "public":
            attrs["zone_type"] = zone_type
            if router_id:
                attrs["router"] = {"router_id": router_id}

        self.zone = self.client.create_zone(**attrs)
        self.client.wait_for_zone(self.zone)
        return self.zone

    def _create_networks(self, count=1):
        created = []
        for _ in range(count):
            network = self.create_network()
            self.networks.append(network)
            created.append(network)
        return created

    def _create_private_zone_with_networks(self, count=1):
        if count < 1:
            raise ValueError("count must be at least 1")

        networks = self._create_networks(count=count)
        zone = self._create_zone(
            zone_name=self.private_zone_alias,
            router_id=networks[0]["router_id"],
            zone_type="private",
        )
        return zone, networks

    def test_list_zones(self):
        self._create_zone(self.public_zone_alias)
        all_zones = list(self.client.zones())
        self.assertGreaterEqual(len(all_zones), 0)

        if all_zones:
            zone = self.client.get_zone(zone=all_zones[0].id)
            self.assertIsNotNone(zone)

    def test_get_zone(self):
        self._create_zone(self.public_zone_alias)
        zone = self.client.get_zone(self.zone.id)
        self.assertEqual(zone.name, self.public_zone_alias)

    def test_find_zone(self):
        self._create_zone(self.public_zone_alias)
        zone = self.client.find_zone(self.zone.name)
        self.assertEqual(zone.name, self.public_zone_alias)

    def test_update_public_zone(self):
        self._create_zone(self.public_zone_alias)
        description = "sdk-test-zone-public-description"
        zone = self.client.update_zone(self.zone.id, description=description)
        self.assertEqual(zone.description, description)

    def test_update_private_zone(self):
        self._create_private_zone_with_networks()
        description = "sdk-test-zone-private-description"
        zone = self.client.update_zone(self.zone.id, description=description)
        self.assertEqual(zone.description, description)

    def test_add_router_to_private_zone(self):
        zone, networks = self._create_private_zone_with_networks(count=2)

        router_1 = networks[0]["router_id"]
        router_2 = networks[1]["router_id"]

        self.client.add_router_to_zone(zone.id, router_id=router_2)
        self.client.wait_for_zone(zone)

        zone = self.client.get_zone(zone.id)
        router_ids = [router["router_id"] for router in zone.routers]

        self.assertIn(router_1, router_ids)
        self.assertIn(router_2, router_ids)

    def test_remove_router_from_private_zone(self):
        zone, networks = self._create_private_zone_with_networks(count=2)

        router_1 = networks[0]["router_id"]
        router_2 = networks[1]["router_id"]

        self.client.add_router_to_zone(zone.id, router_id=router_2)
        self.client.wait_for_zone(zone)

        self.client.remove_router_from_zone(zone.id, router_id=router_2)
        self.client.wait_for_zone(zone)

        zone = self.client.get_zone(zone.id)
        router_ids = [router["router_id"] for router in zone.routers]

        self.assertIn(router_1, router_ids)
        self.assertNotIn(router_2, router_ids)
