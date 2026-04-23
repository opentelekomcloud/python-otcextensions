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

_logger = openstack._log.setup_logging("openstack")


class TestPrivateTransitIp(base.BaseFunctionalTest):

    def test_list_transit_ips(self):
        transit_ips = list(self.conn.natv3.private_transit_ips())
        self.assertGreaterEqual(len(transit_ips), 0)

    def test_get_private_transit_ip(self):
        transit_ip_id = base._get_resource_value("private_transit_ip_id", None)
        if not transit_ip_id:
            self.skipTest("functional.private_transit_ip_id is required")

        transit_ip = self.conn.natv3.get_private_transit_ip(transit_ip_id)
        self.assertEqual(transit_ip_id, transit_ip.id)
