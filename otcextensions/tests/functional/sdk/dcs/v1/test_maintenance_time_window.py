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


class TestMaintenanceTimeWindow(base.BaseFunctionalTest):

    def setUp(self):
        super(TestMaintenanceTimeWindow, self).setUp()
        self.dcs = self.conn.dcs

    def test_maintenance_time_windows(self):
        objects = list(self.dcs.maintenance_time_windows())

        self.assertEqual(len(objects), 6)

        for obj in objects:
            self.assertIsInstance(obj, dict)
            self.assertIn("begin", obj.keys())
            self.assertIn("end", obj.keys())
            self.assertIn("seq", obj.keys())
            self.assertIn("default", obj.keys())
