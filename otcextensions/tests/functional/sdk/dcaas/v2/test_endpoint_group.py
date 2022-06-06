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

    def test_list_endpoint_group(self):
        self._create_endpoint_group()
        endpoint_groups = list(self.dcaas.endpoint_groups())
        self.assertEqual(len(endpoint_groups), 1)
