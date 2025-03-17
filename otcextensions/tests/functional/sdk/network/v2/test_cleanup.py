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

from otcextensions.tests.functional import base


class TestCleanup(base.BaseFunctionalTest):
    def setUp(self):
        super(TestCleanup, self).setUp()
        self.client = self.conn.network

    def test_01_cleanup(self):
        self.client._service_cleanup(dry_run=False)
        netw = list(self.client.networks())
        self.assertEqual(len(netw), 0)
