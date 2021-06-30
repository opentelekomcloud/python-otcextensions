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


class TestRecordsets(TestDns):
    uuid_v4 = uuid.uuid4().hex[:8]
    zone_alias = uuid_v4 + 'dns.sdk-test-zone-public.com.'
    zones = []

    def setUp(self):
        super(TestRecordsets, self).setUp()

        # create public zone
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
        super(TestRecordsets, self).tearDown()

    def test_list_recordsets(self):
        rs = []
        recordsets = self.client.recordsets(self.zone.id)
        for record in recordsets:
            rs.append(record['records'])
        self.assertEqual(rs, [
            ['ns1.open-telekom-cloud.com. '
             'dl-otc-domains.telekom.de. (1 7200 900 1209600 300)'],
            ['ns2.open-telekom-cloud.com.', 'ns1.open-telekom-cloud.com.']])

    def test_create_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'a-record.{self.zone_alias}',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        self.assertEqual(rs.name, f'a-record.{self.zone_alias}')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'aaaa-record.{self.zone_alias}',
            type='AAAA',
            records=['ff03:0db8:85a3:0:0:8a2e:0370:7334']
        )
        self.assertEqual(rs.name, f'aaaa-record.{self.zone_alias}')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'cname-record.{self.zone_alias}',
            type='CNAME',
            records=['www.ex.com']
        )
        self.assertEqual(rs.name, f'cname-record.{self.zone_alias}')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'mx-record.{self.zone_alias}',
            type='MX',
            records=['10 mailserver1.example.com.']
        )
        self.assertEqual(rs.name, f'mx-record.{self.zone_alias}')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'txt-record.{self.zone_alias}',
            type='TXT',
            records=["\"Text.\""]
        )
        self.assertEqual(rs.name, f'txt-record.{self.zone_alias}')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'ns-record.{self.zone_alias}',
            type='NS',
            records=['ns.example.com']
        )
        self.assertEqual(rs.name, f'ns-record.{self.zone_alias}')

    def test_get_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'a-record.{self.zone_alias}',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        record = self.client.get_recordset(
            recordset=rs.id,
            zone=self.zone.id
        )
        self.assertEqual(record.name, f'a-record.{self.zone_alias}')

    def test_find_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'a-record.{self.zone_alias}',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        record = self.client.find_recordset(
            name_or_id=rs.id,
            zone=self.zone.id
        )
        self.assertEqual(record.name, f'a-record.{self.zone_alias}')

    def test_update_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'a-record.{self.zone_alias}',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        record = self.client.update_recordset(
            recordset=rs.id,
            zone_id=self.zone.id,
            description='updated'
        )
        self.assertEqual(record.description, 'updated')

    def test_delete_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name=f'a-record.{self.zone_alias}',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        self.assertEqual(rs.status, 'PENDING_CREATE')
        record = self.client.delete_recordset(
            recordset=rs.id,
            zone=self.zone.id
        )
        self.assertIsNotNone(record)
