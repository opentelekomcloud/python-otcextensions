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

from otcextensions.tests.functional.sdk.ctsv3 import TestCtsv3


class TestQuotas(TestCtsv3):
    def setUp(self):
        super(TestQuotas, self).setUp()
        self.cts = self.conn.ctsv3

    def test_01_list_quotas(self):
        quotas = list(self.cts.quotas())
        self.assertIsNotNone(quotas)
