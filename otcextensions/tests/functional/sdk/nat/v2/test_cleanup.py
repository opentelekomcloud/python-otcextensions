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
from openstack import _log


from otcextensions.tests.functional import base

_logger = _log.setup_logging('openstack')


class TestCleanup(base.BaseFunctionalTest):
    def setUp(self):
        super(TestCleanup, self).setUp()

    def test_01_delete(self):
        gateways = list(self.conn.nat.gateways())
        self.conn.nat._service_cleanup(dry_run=False)
        gateways = list(self.conn.nat.gateways())
        self.assertEqual(len(gateways), 0)
