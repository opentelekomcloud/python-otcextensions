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

from otcextensions.tests.functional.sdk.dns import TestDns

_logger = openstack._log.setup_logging('openstack')


class TestZone(TestDns):
    PUBLIC_ZONE_ALIAS = 'dns.sdk-test-zone-public.com.'
    PRIVATE_ZONE_ALIAS = 'dns.sdk-test-zone-private.com.'
    zones = []

    def setUp(self):
        super(TestZone, self).setUp()

        self.create_network()
        # create public zone
        try:
            self.zone = self.client.create_zone(name=TestZone.PUBLIC_ZONE_ALIAS)
        except openstack.exceptions.BadRequestException:
            self.zone = self.client.find_zone(TestZone.PUBLIC_ZONE_ALIAS)
        self.zones.append(self.zone)

        # create private zone
        try:
            self.private_zone = self.client.create_zone(
                name=TestZone.PRIVATE_ZONE_ALIAS,
                router={'router_id': self.router_id},
                zone_type = "private"
            )
        except openstack.exceptions.BadRequestException:
            self.private_zone = self.client.find_zone(TestZone.PRIVATE_ZONE_ALIAS)
        self.zones.append(self.private_zone)

    def tearDown(self):
        super(TestZone, self).tearDown()
        try:
            for zone in self.zones:
                if zone:
                    self.client.delete_zone(zone)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        self.destroy_network()

    def test_list_zones(self):
        self.all_zones = list(self.client.zones())
        self.assertGreaterEqual(len(self.all_zones), 0)
        if len(self.all_zones) > 0:
            zone = self.all_zones[0]
            zone = self.client.get_zone(zone=zone.id)
            self.assertIsNotNone(zone)

    def test_get_zone(self):
        zone = self.client.get_zone(self.zone.id)
        self.assertEqual(zone.name, self.PUBLIC_ZONE_ALIAS)

    def test_find_zone(self):
        zone = self.client.find_zone(self.zone.name)
        self.assertEqual(zone.name, self.PUBLIC_ZONE_ALIAS)

    def test_update_public_zone(self):
        description = 'sdk-test-zone-public-description'
        zone = self.client.update_zone(self.zone.id, description=description)
        self.assertEqual(zone.description, description)

    def test_update_private_zone(self):
        description = 'sdk-test-zone-private-description'
        zone = self.client.update_zone(self.private_zone.id, description=description)
        self.assertEqual(zone.description, description)

    def test_add_router_to_private_zone(self):
        self.add_rt_id, self.add_sub_id, self.add_net_id = self.create_additional_network()
        zone = self.client.add_router_to_zone(
            self.private_zone.id,
            router_id=self.add_rt_id
        )
        self.destroy_additional_network(self.add_rt_id, self.add_sub_id, self.add_net_id)
        self.assertEqual(json.loads(zone.text)['router_id'], self.add_rt_id)
        self.assertEqual(json.loads(zone.text)['status'], 'PENDING_CREATE')

    def test_remove_router_from_private_zone(self):
        self.add_rt_id, self.add_sub_id, self.add_net_id = self.create_additional_network()
        self.client.add_router_to_zone(
            self.private_zone.id,
            router_id=self.add_rt_id
        )
        zone = self.client.remove_router_from_zone(
            self.private_zone.id,
            router_id=self.add_rt_id
        )
        self.destroy_additional_network(self.add_rt_id, self.add_sub_id, self.add_net_id)
        self.assertEqual(json.loads(zone.text)['router_id'], self.add_rt_id)
        self.assertEqual(json.loads(zone.text)['status'], 'PENDING_DELETE')
