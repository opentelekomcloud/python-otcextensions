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
import uuid

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestQuota(TestVlb):
    uuid_v4 = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestQuota, self).setUp()

    def test_get_quotas(self):
        qt = self.client.quotas()
        self.assertGreaterEqual(len(qt), 0)
