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
import json
import openstack
import uuid

from otcextensions.tests.functional.sdk.dns import TestDns

_logger = openstack._log.setup_logging('openstack')


class TestZone(TestDns):
    uuid_v4 = uuid.uuid4().hex[:8]
    public_zone_alias = uuid_v4 + 'dns.sdk-test-zone-public.com.'
    private_zone_alias = uuid_v4 + 'dns.sdk-test-zone-private.com.'

    def setUp(self):
        super(TestZone, self).setUp()

    def tearDown(self):
        super(TestZone, self).tearDown()
        try:
            if self.zone:
                self.client.delete_zone(self.zone)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def _create_zone(self, zone_name=None, router_id=None, zone_type='public'):
        if zone_type != 'public' and router_id:
            try:
                self.zone = self.client.create_zone(
                    name=zone_name,
                    router={'router_id': router_id},
                    zone_type=zone_type
                )
            except openstack.exceptions.BadRequestException:
                self.zone = self.client.find_zone(zone_name)
            return
        try:
            self.zone = self.client.create_zone(
                name=zone_name
            )
        except openstack.exceptions.BadRequestException:
            self.zone = self.client.find_zone(zone_name)

    def _create_multiple_networks(self, count=1):
        networks = []
        for i in range(count):
            network = self.create_network()
            networks.append(network)
        return networks

    def test_01_list_zones(self):
        self._create_zone(self.public_zone_alias)
        self.all_zones = list(self.client.zones())
        self.assertGreaterEqual(len(self.all_zones), 0)
        if len(self.all_zones) > 0:
            zone = self.all_zones[0]
            zone = self.client.get_zone(zone=zone.id)
            self.assertIsNotNone(zone)

    def test_02_get_zone(self):
        self._create_zone(self.public_zone_alias)
        zone = self.client.get_zone(self.zone.id)
        self.assertEqual(zone.name, self.public_zone_alias)

    def test_03_find_zone(self):
        self._create_zone(self.public_zone_alias)
        zone = self.client.find_zone(self.zone.name)
        self.assertEqual(zone.name, self.public_zone_alias)

    def test_04_update_public_zone(self):
        self._create_zone(self.public_zone_alias)
        description = 'sdk-test-zone-public-description'
        zone = self.client.update_zone(self.zone.id, description=description)
        self.assertEqual(zone.description, description)

    def test_05_update_private_zone(self):
        network = self.create_network()
        # create private zone
        self._create_zone(
            zone_name=self.private_zone_alias,
            router_id=network['router_id'],
            zone_type='private'
        )
        description = 'sdk-test-zone-private-description'
        zone = self.client.update_zone(
            self.zone.id,
            description=description
        )
        self.destroy_network(network)
        self.assertEqual(zone.description, description)

    def test_06_add_router_to_private_zone(self):
        networks = self._create_multiple_networks(count=2)
        self._create_zone(
            zone_name=self.private_zone_alias,
            router_id=networks[0]['router_id'],
            zone_type='private'
        )
        zone = self.client.add_router_to_zone(
            self.zone.id,
            router_id=networks[1]['router_id']
        )
        for network in networks:
            self.destroy_network(network)
        self.assertEqual(
            json.loads(zone.text)['router_id'],
            networks[1]['router_id']
        )
        self.assertEqual(json.loads(zone.text)['status'], 'PENDING_CREATE')

    def test_07_remove_router_from_private_zone(self):
        networks = self._create_multiple_networks(count=2)
        # create private zone
        self._create_zone(
            zone_name=self.private_zone_alias,
            router_id=networks[0]['router_id'],
            zone_type='private'
        )
        zone = self.client.add_router_to_zone(
            self.zone.id,
            router_id=networks[1]['router_id']
        )
        self.assertIsNotNone(zone)
        zone = self.client.remove_router_from_zone(
            self.zone.id,
            router_id=networks[1]['router_id']
        )
        for network in networks:
            self.destroy_network(network)
        self.assertEqual(
            json.loads(zone.text)['router_id'],
            networks[1]['router_id']
        )
        self.assertEqual(json.loads(zone.text)['status'], 'PENDING_DELETE')
