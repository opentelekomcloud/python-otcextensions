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


class TestPrivateSnat(base.BaseFunctionalTest):

    def test_list_snat_rules(self):
        snat_rules = list(self.conn.natv3.private_snat_rules())
        self.assertGreaterEqual(len(snat_rules), 0)

    def test_get_private_snat_rule(self):
        snat_rules = list(self.conn.natv3.private_snat_rules(limit=1))
        if not snat_rules:
            self.skipTest("No private SNAT rules available for fetch test")

        snat_rule = self.conn.natv3.get_private_snat_rule(snat_rules[0].id)
        self.assertEqual(snat_rule.id, snat_rules[0].id)
