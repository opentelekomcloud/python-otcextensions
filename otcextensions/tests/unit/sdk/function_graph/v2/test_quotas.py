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

from otcextensions.sdk.function_graph.v2 import quota

EXAMPLE = {
    "quotas": {
        "resources": [{
            "quota": 60,
            "used": 3,
            "type": "fgs_func_scale_down_timeout"
        }, {
            "quota": 100,
            "used": 22,
            "type": "fgs_func_occurs"
        }, {
            "quota": 100,
            "used": 22,
            "type": "fgs_func_pat_idle_time"
        }, {
            "quota": 100,
            "used": 22,
            "type": "fgs_func_num"
        }, {
            "quota": 10240,
            "used": 22,
            "type": "fgs_func_code_size",
            "unit": "MB"
        }, {
            "quota": 512,
            "used": 22,
            "type": "fgs_workflow_num"
        }]
    }
}


class TestFunctionQuota(base.TestCase):

    def test_basic(self):
        sot = quota.Quota()
        path = '/fgs/quotas'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = quota.Quota(**EXAMPLE)
        self.assertEqual(EXAMPLE['quotas'], sot.quotas)
