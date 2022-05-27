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


class TestAvailabilityZone(base.BaseFunctionalTest):

    def setUp(self):
        super(TestAvailabilityZone, self).setUp()
        self.dcs = self.conn.dcs

    def test_availability_zone(self):
        objects = list(self.dcs.availability_zones())

        self.assertEqual(len(objects), 3)

        for obj in objects:
            self.assertIsInstance(obj, dict)
            self.assertIn("id", obj.keys())
            self.assertIn("code", obj.keys())
            self.assertIn("name", obj.keys())
            self.assertIn("port", obj.keys())
            self.assertIn("resource_availability", obj.keys())
