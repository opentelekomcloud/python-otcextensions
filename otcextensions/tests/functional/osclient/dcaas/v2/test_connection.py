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

from openstackclient.tests.functional import base


class TestDirectConnection(base.TestCase):

    UUID = uuid.uuid4().hex[:8]
    DC_NAME = "direct_connect-" + UUID
    BANDWIDTH = 50
    PORT_TYPE = "1G"
    PROVIDER = "OTC"
    LOCATION = "Biere"

    def setUp(self):
        super(TestDirectConnection, self).setUp()

    def tearDown(self):
        try:
            if self.DC_ID:
                self._delete_direct_connection()
        finally:
            super(TestDirectConnection, self).tearDown()

    def _create_direct_connection(self):
        json_output = json.loads(self.openstack(
            'dcaas connection create'
            ' {port_type}'
            ' {bandwidth}'
            ' {location}'
            ' {provider}'
            ' --name {name} -f json'.format(
                name=self.DC_NAME,
                port_type=self.PORT_TYPE,
                bandwidth=self.BANDWIDTH,
                location=self.LOCATION,
                provider=self.PROVIDER
            )
        ))
        self.DC_ID = json_output['id']
        return json_output

    def _delete_direct_connection(self):
        self.openstack('dcaas connection delete ' + self.DC_ID)

    def test_create_direct_connection(self):
        json_output = self._create_direct_connection()
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['id'], self.DC_ID)

    def test_list_direct_connection(self):
        self._create_direct_connection()
        json_output = json.loads(self.openstack(
            'dcaas connection list -f json'
        ))
        self.assertIsNotNone(json_output)

    def test_list_filter_direct_connection(self):
        self._create_direct_connection()
        json_output = json.loads(self.openstack(
            'dcaas connection list '
            '--name {name} '
            '--bandwidth {bandwidth} '
            '--port_type {port_type} '
            '--location {location} '
            '--provider {provider} -f json'.format(
                name=self.DC_NAME,
                bandwidth=self.BANDWIDTH,
                port_type=self.PORT_TYPE,
                location=self.LOCATION,
                provider=self.PROVIDER
            )
        ))
        self.assertIsNotNone(json_output)

    def test_find_direct_connection(self):
        self._create_direct_connection()
        json_output = json.loads(self.openstack(
            'dcaas connection show {id} -f json'.format(id=self.DC_ID)
        ))
        self.assertIsNotNone(json_output)

    def test_update_direct_connection(self):
        self._create_direct_connection()
        connection_name = self.DC_NAME + '-updated'
        json_output = json.loads(self.openstack(
            'dcaas connection update {id} --name {name} -f json'.format(
                id=self.DC_ID,
                name=connection_name
            )
        ))
        self.assertEqual(json_output['id'], self.DC_ID)
        self.assertEqual(json_output['name'], connection_name)
