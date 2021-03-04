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
from otcextensions.tests.functional import base
from datetime import datetime

_logger = openstack._log.setup_logging('openstack')


class TestGateway(base.BaseFunctionalTest):
    CURR_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def setUp(self):
        super(TestGateway, self).setUp()

    def test_list(self):
        gateways = list(self.conn.nat.gateways())
        self.assertGreaterEqual(len(gateways), 0)

    def test_list_filters(self):
        attrs = {
            'limit': 1,
            'id': '2',
            'name': '3',
            'spec': '4',
            'router_id': '5',
            'internal_network_id': '6',
            'project_id': '7',
            'status': 'active',
            'admin_state_up': True,
            'created_at': self.CURR_TIME
        }
        gateways = list(self.conn.nat.gateways(**attrs))
        self.assertGreaterEqual(len(gateways), 0)
