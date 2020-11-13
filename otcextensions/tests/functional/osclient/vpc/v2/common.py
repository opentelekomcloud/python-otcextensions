#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import json
import uuid

from datetime import datetime

from openstackclient.tests.functional import base


class VpcTestCase(base.TestCase):
    """Common functional test bits for VPC commands"""

    CURR_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def setUp(self):
        super(VpcTestCase, self).setUp()
        UUID = uuid.uuid4().hex[:8]
        self.LOCAL_ROUTER_NAME = 'test-local-router-otce-cli' + UUID
        self.PEER_ROUTER_NAME = 'test-peer-router-otce-cli' + UUID
        self.PEERING_NAME = 'test-peering-otce-cli-' + UUID

        self.LOCAL_ROUTER_ID = None
        self.PEER_ROUTER_ID = None
        self.PEERING_ID = None

    def create_vpc_peering(self, name=None):
        self._create_routers()
        name = name or self.PEERING_NAME
        json_output = json.loads(self.openstack(
            'vpc peering create '
            '{name} '
            '--local-router-id "{local_router_id}" '
            '--peer-router-id "{peer_router_id}" '
            '-f json'.format(
                name=name,
                local_router_id=self.LOCAL_ROUTER_ID,
                peer_router_id=self.PEER_ROUTER_ID)
        ))
        self.assertIsNotNone(json_output)
        self.PEERING_ID = json_output['id']
        return json_output

    def delete_vpc_peering(self):
        self.addCleanup(self._delete_routers)
        self.openstack('vpc peering delete {}'.format(self.PEERING_ID))

    def _create_routers(self):
        local_router = json.loads(self.openstack(
            'router create -f json ' + self.LOCAL_ROUTER_NAME
        ))
        self.LOCAL_ROUTER_ID = local_router['id']

        peer_router = json.loads(self.openstack(
            'router create -f json ' + self.PEER_ROUTER_NAME
        ))
        self.PEER_ROUTER_ID = peer_router['id']

    def _delete_routers(self):
        self.openstack(
            'router delete {} {}'.format(
                self.LOCAL_ROUTER_ID, self.PEER_ROUTER_ID
            ))
