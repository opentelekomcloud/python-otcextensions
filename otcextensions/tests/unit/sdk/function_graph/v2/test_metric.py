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

from otcextensions.sdk.function_graph.v2 import metric


EXAMPLE = {
    'duration': [
        {
            'timestamp': 1596679200000,
            'value': -1
        }
    ],
}


class TestFunctionInvocation(base.TestCase):

    def test_basic(self):
        sot = metric.Metric()
        path = '/fgs/functions/statistics'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = metric.Metric(**EXAMPLE)
        self.assertEqual(EXAMPLE['duration'][0]['timestamp'], sot.duration[0].timestamp)
        self.assertEqual(EXAMPLE['duration'][0]['value'], sot.duration[0].value)
