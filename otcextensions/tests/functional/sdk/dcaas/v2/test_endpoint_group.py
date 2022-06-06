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

from otcextensions.tests.functional.sdk.dcaas.v2 import base

_logger = openstack._log.setup_logging('openstack')


class TestDirectConnectEndpointGroup(base.BaseDCTest):

    UUID = base.BaseDCTest.UUID
    CIDR = base.BaseDCTest.CIDR
    TYPE = "cidr"
    EG_NAME = "test-eg-" + UUID

    def setUp(self):
        super(TestDirectConnectEndpointGroup, self).setUp()
        self.dcaas = self.conn.dcaas
        self._create_endpoint_group()

    def tearDown(self):
        try:
            self._delete_endpoint_group()
        finally:
            super(TestDirectConnectEndpointGroup, self).tearDown()

    def _create_endpoint_group(self):
        project_id = self.conn.session.get_project_id()
        endpoints = [self.CIDR]
        self.endpoint_group = self.dcaas.create_endpoint_group(
            project_id=project_id,
            name=self.EG_NAME,
            endpoints=endpoints,
            type=self.TYPE
        )

    def _delete_endpoint_group(self):
        if self.endpoint_group:
            self.dcaas.delete_endpoint_group(self.endpoint_group.id)

    def test_create_and_get_endpoint_group(self):
        endpoint_group = self.dcaas.get_endpoint_group(self.endpoint_group.id)
        self.assertEqual(endpoint_group.name, self.EG_NAME)

    def test_list_endpoint_group(self):
        endpoint_groups = list(self.dcaas.endpoint_groups())
        self.assertEqual(len(endpoint_groups), 1)

    def test_find_and_update_endpoint_group(self):
        updated_name = "updated_name"
        endpoint_group = self.dcaas.find_endpoint_group(self.EG_NAME)
        updated_ep_group = self.dcaas.update_endpoint_group(
            endpoint_group=endpoint_group,
            name=updated_name
        )
        self.assertEqual(self.endpoint_group.id, endpoint_group.id)
        self.assertEqual(endpoint_group.id, updated_ep_group.id)
        self.assertEqual(updated_ep_group.name, updated_name)
