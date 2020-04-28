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


class TestDnat(base.BaseFunctionalTest):
    CURR_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    def setUp(self):
        super(TestDnat, self).setUp()
        openstack.enable_logging(debug=True, http_debug=True)

    def test_list(self):
        gateways = list(self.conn.nat.dnat_rules())
        self.assertGreaterEqual(len(gateways), 0)

    def test_list_filters(self):
        attrs = {
            'limit': 1,
            'id': '2',
            'project_id': '3',
            'port_id': '4',
            'private_ip': '5',
            'internal_service_port': '6',
            'floating_ip_id': '7',
            'floating_ip_address': '8',
            'external_service_port': '9',
            'nat_gateway_id': '11',
            'protocol': 'tcp',
            'status': 'active',
            'admin_state_up': True,
            'created_at': self.CURR_TIME
        }
        gateways = list(self.conn.nat.dnat_rules(**attrs))
        self.assertGreaterEqual(len(gateways), 0)
