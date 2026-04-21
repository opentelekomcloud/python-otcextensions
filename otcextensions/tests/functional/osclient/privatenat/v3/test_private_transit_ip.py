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

from openstackclient.tests.functional import base


class TestPrivateTransitIp(base.TestCase):
    """Functional Tests for private NAT transit IP addresses"""

    def setUp(self):
        super(TestPrivateTransitIp, self).setUp()

    def test_privatenat_transit_ip_list(self):
        json_output = json.loads(self.openstack("privatenat transit ip list -f json "))
        self.assertIsNotNone(json_output)
