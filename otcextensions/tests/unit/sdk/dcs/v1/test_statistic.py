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
import mock

from keystoneauth1 import adapter

from openstack.tests.unit import base

from otcextensions.sdk.dcs.v1 import statistic

FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "keys": 0,
    "instance_id": "e008652d-18e0-43ff-924e-072261e0372a",
    "used_memory": 0,
    "max_memory": 460,
    "cmd_get_count": 0,
    "cmd_set_count": 0,
    "used_cpu": "0.0",
    "input_kbps": "0.03",
    "output_kbps": "1.19"
}


class TestStatistics(base.TestCase):

    def setUp(self):
        super(TestStatistics, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.put = mock.Mock()

    def test_basic(self):
        sot = statistic.Statistic()

        self.assertEqual('/instances/statistic', sot.base_path)

        self.assertTrue(sot.allow_list)

    def test_make_it(self):

        sot = statistic.Statistic(**EXAMPLE)
        self.assertEqual(EXAMPLE['instance_id'], sot.id)
        self.assertEqual(EXAMPLE['keys'], sot.keys)
        self.assertEqual(EXAMPLE['used_memory'], sot.used_memory)
        self.assertEqual(EXAMPLE['max_memory'], sot.max_memory)
        self.assertEqual(EXAMPLE['cmd_get_count'], sot.cmd_get_count)
        self.assertEqual(EXAMPLE['cmd_set_count'], sot.cmd_set_count)
        self.assertEqual(EXAMPLE['used_cpu'], sot.used_cpu)
        self.assertEqual(EXAMPLE['input_kbps'], sot.input_kbps)
        self.assertEqual(EXAMPLE['output_kbps'], sot.output_kbps)
