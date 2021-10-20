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

from otcextensions.sdk.vlb.v3 import l7_rule

EXAMPLE = {
    'compare_type': 'compare_type',
    'admin_state_up': True,
    'value': 'value',
    'type': 'type',
}


class TestLoadBalancer(base.TestCase):

    def test_basic(self):
        sot = l7_rule.L7Rule()
        path = '/elb/l7policies/%(l7policy_id)s/rules'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = l7_rule.L7Rule(**EXAMPLE)
        self.assertEqual(EXAMPLE['compare_type'], sot.compare_type)
        self.assertEqual(EXAMPLE['value'], sot.rule_value)
        self.assertEqual(EXAMPLE['type'], sot.type)
