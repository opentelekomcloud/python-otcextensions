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
import random

from otcextensions.tests.functional.sdk.dds import TestDds


class TestInstance(TestDds):
    def setUp(self):
        super(TestInstance, self).setUp()

    def test_01_get_policies(self):
        result = self.client.get_policy()
        self.assertIsNotNone(result)

    def test_02_set_policy(self):
        new_number = random.randrange(1, 7)
        attrs = {
            "enabled": True,
            "retention_period_in_days": new_number
        }
        self.client.create_policy(**attrs)
        result = self.client.get_policy()
        self.assertEqual(new_number, result['retention_period_in_days'])
