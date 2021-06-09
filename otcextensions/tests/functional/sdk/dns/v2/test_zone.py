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

from otcextensions.tests.functional.sdk.dns import TestDns

_logger = openstack._log.setup_logging('openstack')


class TestZone(TestDns):
    ZONE_ALIAS = 'dns.sdk-test-zone.com.'
    zones = []

    def setUp(self):
        super(TestZone, self).setUp()

        # self.create_network()
        try:
            self.zone = self.client.create_zone(name=TestZone.ZONE_ALIAS)
        except openstack.exceptions.BadRequestException:
            self.zone = self.client.find_zone(TestZone.ZONE_ALIAS)
        print(f'Created: {self.zone}')
        self.zones.append(self.zone)

    def tearDown(self):
        super(TestZone, self).tearDown()
        # self.destroy_network()
        try:
            for zone in self.zones:
                if zone.id:
                    self.client.delete_zone(zone)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

    def test_list(self):
        self.all_zones = list(self.conn.dns.zones())
        self.assertGreaterEqual(len(self.all_zones), 0)
        if len(self.all_zones) > 0:
            zone = self.all_zones[0]
            zone = self.client.get_zone(zone=zone.id)
            self.assertIsNotNone(zone)
