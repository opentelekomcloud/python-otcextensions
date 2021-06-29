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
import uuid

from otcextensions.tests.functional.sdk.dns import TestDns

_logger = openstack._log.setup_logging('openstack')


class TestNameservers(TestDns):
    uuid_v4 = uuid.uuid4().hex[:8]
    zone_alias = uuid_v4 + 'dns.sdk-test-zone-public.com.'
    zones = []

    def setUp(self):
        super(TestNameservers, self).setUp()
        # create zone
        try:
            self.zone = self.client.create_zone(
                name=self.zone_alias
            )
        except openstack.exceptions.BadRequestException:
            self.zone = self.client.find_zone(self.zone_alias)
        self.zones.append(self.zone)

    def tearDown(self):
        try:
            for zone in self.zones:
                if zone:
                    self.client.delete_zone(zone)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        finally:
            super(TestNameservers, self).tearDown()

    def test_list_nameservers(self):
        nameservers = []
        zone = self.client.nameservers(zone=self.zone.id)
        self.assertIsNotNone(zone)
        for ns in zone:
            nameservers.append(ns['hostname'])
        self.assertEqual(nameservers,
                         ['ns1.open-telekom-cloud.com.',
                          'ns2.open-telekom-cloud.com.'])
