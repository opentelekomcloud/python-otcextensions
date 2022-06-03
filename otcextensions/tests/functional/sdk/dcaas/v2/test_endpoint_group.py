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

from otcextensions.tests.functional.sdk.dcaas.v2 import base

_logger = openstack._log.setup_logging('openstack')


class TestDirectConnectEndpointGroup(base.BaseDCTest):

    def setUp(self):
        super(TestDirectConnectEndpointGroup, self).setUp()
        self.dcaas = self.conn.dcaas

    def tearDown(self):
        super(TestDirectConnectEndpointGroup, self).setUp()

    def test_list_endpoint_group(self):
        endpoint_groups = list(self.dcaas.endpoint_groups())
        self.assertGreaterEqual(len(endpoint_groups), 0)
