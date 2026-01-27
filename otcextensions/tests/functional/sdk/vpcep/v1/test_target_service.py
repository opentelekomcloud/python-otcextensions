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
from otcextensions.tests.functional.sdk.vpcep import TestVpcep


class TestTargetService(TestVpcep):
    """Tests for target service lookup (requires Service)."""

    def setUp(self):
        super(TestTargetService, self).setUp()
        self.service = self.create_service_helper()

    def test_get_target_service_by_id(self):
        """Test getting a Target Service by ID."""
        target = self.client.get_target_service(self.service.id)
        self.assertIsNotNone(target)
        self.assertEqual(self.service.id, target.id)

    def test_get_target_service_by_name(self):
        """Test getting a Target Service by name."""
        target = self.client.get_target_service(self.service.service_name)
        self.assertIsNotNone(target)
        self.assertEqual(self.service.service_name, target.service_name)
