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
import time

from otcextensions.tests.functional.sdk.vpcep import TestVpcep


class TestWhitelist(TestVpcep):

    def setUp(self):
        super(TestWhitelist, self).setUp()
        self.network_data = self.create_network()
        self.addCleanup(self.destroy_network, self.network_data)
        self.port = self.create_port(self.network_data['network_id'])
        self.addCleanup(self.destroy_port, self.port.id)
        self.service = self.create_service_helper(approval=True)
        self.target_domain = self.conn.current_project_id
        if not self.target_domain and hasattr(self.conn, 'session'):
            self.target_domain = self.conn.session.get_project_id()

    def _add_whitelist(self, domains):
        return list(self.client.manage_service_whitelist(self.service.id,
                                                         action='add',
                                                         domains=domains))

    def test_add_service_whitelist(self):
        """Test adding a domain to the whitelist."""
        if not self.target_domain:
            self.skipTest("Cannot determine current project"
                          " ID for whitelist test")

        domains = [self.target_domain]
        added = self._add_whitelist(domains)
        found = any([domains[0] in (w.permission or '') for w in added])
        self.assertTrue(found, "Domain not found in added whitelist")

    def test_add_service_whitelist_duplicate(self):
        """Test adding a duplicate domain to the whitelist."""
        if not self.target_domain:
            self.skipTest("Cannot determine current"
                          " project ID for whitelist test")

        domains = [self.target_domain]
        self._add_whitelist(domains)

        self._add_whitelist(domains)

        listed = list(self.client.service_whitelist(self.service.id))
        found = any([domains[0] in (w.permission or '') for w in listed])
        self.assertTrue(found, "Domain not found "
                               "in whitelist after duplicate add")

    def test_list_service_whitelist(self):
        """Test listing the whitelist."""
        if not self.target_domain:
            self.skipTest("Cannot determine current project ID"
                          " for whitelist test")

        domains = [self.target_domain]
        self._add_whitelist(domains)

        listed = list(self.client.service_whitelist(self.service.id))
        self.assertGreater(len(listed), 0)
        found = any([domains[0] in (w.permission or '') for w in listed])
        self.assertTrue(found, "Domain not found in listed whitelist")

    def test_remove_service_whitelist(self):
        """Test removing a domain from the whitelist."""
        if not self.target_domain:
            self.skipTest("Cannot determine current project ID"
                          " for whitelist test")

        domains = [self.target_domain]
        self._add_whitelist(domains)

        list(self.client.manage_service_whitelist(self.service.id,
                                                  action='remove',
                                                  domains=domains))

        time.sleep(5)

        listed_after = list(self.client.service_whitelist(self.service.id))
        found = any([domains[0] in (w.permission or '') for w in listed_after])
        self.assertFalse(found,
                         "Domain still found in whitelist after removal")
