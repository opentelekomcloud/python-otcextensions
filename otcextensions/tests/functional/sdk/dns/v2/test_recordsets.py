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


class TestRecordsets(TestDns):
    PUBLIC_ZONE_ALIAS = 'dns.sdk-test-zone-public.com.'
    zones = []

    def setUp(self):
        super(TestRecordsets, self).setUp()

        # create public zone
        try:
            self.zone = self.client.create_zone(
                name=TestRecordsets.PUBLIC_ZONE_ALIAS
            )
        except openstack.exceptions.BadRequestException:
            self.zone = self.client.find_zone(TestRecordsets.PUBLIC_ZONE_ALIAS)
        self.zones.append(self.zone)

    def tearDown(self):
        super(TestRecordsets, self).tearDown()
        try:
            for zone in self.zones:
                if zone:
                    self.client.delete_zone(zone)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)

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
            name='a-record.dns.sdk-test-zone-public.com.',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        self.assertEqual(rs.name, 'a-record.dns.sdk-test-zone-public.com.')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='aaaa-record.dns.sdk-test-zone-public.com.',
            type='AAAA',
            records=['ff03:0db8:85a3:0:0:8a2e:0370:7334']
        )
        self.assertEqual(rs.name, 'aaaa-record.dns.sdk-test-zone-public.com.')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='cname-record.dns.sdk-test-zone-public.com.',
            type='CNAME',
            records=['www.ex.com']
        )
        self.assertEqual(rs.name, 'cname-record.dns.sdk-test-zone-public.com.')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='mx-record.dns.sdk-test-zone-public.com.',
            type='MX',
            records=['10 mailserver1.example.com.']
        )
        self.assertEqual(rs.name, 'mx-record.dns.sdk-test-zone-public.com.')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='txt-record.dns.sdk-test-zone-public.com.',
            type='TXT',
            records=["\"Text.\""]
        )
        self.assertEqual(rs.name, 'txt-record.dns.sdk-test-zone-public.com.')

        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='ns-record.dns.sdk-test-zone-public.com.',
            type='NS',
            records=['ns.example.com']
        )
        self.assertEqual(rs.name, 'ns-record.dns.sdk-test-zone-public.com.')

    def test_get_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='a-record.dns.sdk-test-zone-public.com.',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        record = self.client.get_recordset(
            recordset=rs.id,
            zone=self.zone.id
        )
        self.assertEqual(record.name, 'a-record.dns.sdk-test-zone-public.com.')

    def test_find_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='a-record.dns.sdk-test-zone-public.com.',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        record = self.client.find_recordset(
            name_or_id=rs.id,
            zone=self.zone.id
        )
        self.assertEqual(record.name, 'a-record.dns.sdk-test-zone-public.com.')

    def test_update_recordset(self):
        rs = self.client.create_recordset(
            zone=self.zone.id,
            name='a-record.dns.sdk-test-zone-public.com.',
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
            name='a-record.dns.sdk-test-zone-public.com.',
            type='A',
            records=['1.1.1.1', '2.2.2.2']
        )
        self.assertEqual(rs.status, 'PENDING_CREATE')
        record = self.client.delete_recordset(
            recordset=rs.id,
            zone=self.zone.id
        )
        self.assertIsNotNone(record)
