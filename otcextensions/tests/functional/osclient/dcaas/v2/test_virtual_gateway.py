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

from otcextensions.tests.functional.osclient.dcaas.v2 import common


class TestVirtualGateway(common.DcaasTestCase):

    UUID = uuid.uuid4().hex[:8]
    VG_NAME = "gateway-" + UUID

    def setUp(self):
        super(TestVirtualGateway, self).setUp()

    def tearDown(self):
        try:
            self._delete_virtual_gateway()
        finally:
            super(TestVirtualGateway, self).tearDown()

    def _create_virtual_gateway(self):
        json_output = json.loads(self.openstack(
            'dcaas gateway create '
            '{vpc_id} '
            '{local_ep_group_id} '
            '--name {name} -f json '.format(
                name=self.VG_NAME,
                vpc_id=self.VPC_ID,
                local_ep_group_id=self.EP_GROUP_ID
            )
        ))
        self.VG_ID = json_output['id']
        return json_output

    def _delete_virtual_gateway(self):
        self.openstack('dcaas gateway delete ' + self.VG_ID)

    def test_create_virtual_gateway(self):
        json_output = self._create_virtual_gateway()
        self.assertIsNotNone(json_output)
        self.assertEqual(json_output['id'], self.VG_ID)

    def test_list_virtual_gateway(self):
        self._create_virtual_gateway()
        json_output = json.loads(self.openstack(
            'dcaas gateway list -f json'
        ))
        self.assertIsNotNone(json_output)

    def test_list_filter_virtual_gateway(self):
        self._create_virtual_gateway()
        json_output = json.loads(self.openstack(
            'dcaas gateway list '
            '--name {name} '
            '--vpc_id {vpc_id} '
            '--local_ep_group_id {local_ep_group_id} -f json'.format(
                name=self.VG_NAME,
                vpc_id=self.VPC_ID,
                local_ep_group_id=self.EP_GROUP_ID
            )
        ))
        self.assertIsNotNone(json_output)

    def test_find_virtual_gateway(self):
        self._create_virtual_gateway()
        json_output = json.loads(self.openstack(
            'dcaas gateway show {id} -f json'.format(id=self.VG_ID)
        ))
        self.assertIsNotNone(json_output)

    def test_update_virtual_gateway(self):
        self._create_virtual_gateway()
        gateway_name = self.VG_NAME + '-updated'
        json_output = json.loads(self.openstack(
            'dcaas gateway update {id} --name {name} -f json'.format(
                id=self.VG_ID,
                name=gateway_name
            )
        ))
        self.assertEqual(json_output['id'], self.VG_ID)
        self.assertEqual(json_output['name'], gateway_name)
