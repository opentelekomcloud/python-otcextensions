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

from openstack.tests.unit import base

from otcextensions.sdk.dds.v3 import recycle_policy

EXAMPLE = {
    "enabled": True,
    "retention_period_in_days": 3
}


class TestRecyclePolicy(base.TestCase):
    def test_basic(self):
        sot = recycle_policy.RecyclePolicy()
        path = 'instances/recycle-policy'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)

    def test_make_it(self):
        sot = recycle_policy.RecyclePolicy(**EXAMPLE)
        self.assertEqual(EXAMPLE['enabled'], sot.enabled)
        self.assertEqual(EXAMPLE['retention_period_in_days'],
                         sot.retention_period_in_days)
