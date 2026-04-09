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


class TestPrivateDnat(base.BaseFunctionalTest):

    def test_list_dnat_rules(self):
        self.dnat_rules = list(self.conn.natv3.private_dnat_rules())
        self.assertGreaterEqual(len(self.dnat_rules), 0)

    def test_get_private_dnat_rule(self):
        dnat_rules = list(self.conn.natv3.private_dnat_rules(limit=1))
        if not dnat_rules:
            self.skipTest("No private DNAT rules available for fetch test")

        dnat_rule = self.conn.natv3.get_private_dnat_rule(dnat_rules[0].id)
        self.assertEqual(dnat_rule.id, dnat_rules[0].id)
