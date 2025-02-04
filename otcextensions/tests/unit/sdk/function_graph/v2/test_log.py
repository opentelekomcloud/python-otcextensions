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

from otcextensions.sdk.function_graph.v2 import log


EXAMPLE = {
    'group_name': 'group-xxx',
    'group_id': 'xxx',
    'stream_id': 'id-xxx',
    'stream_name': 'xxx'
}


class TestFunctionInvocation(base.TestCase):

    def test_basic(self):
        sot = log.Log()
        path = '/fgs/functions/%(function_urn)s/lts-log-detail'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = log.Log(**EXAMPLE)
        self.assertEqual(EXAMPLE['group_name'], sot.group_name)
        self.assertEqual(EXAMPLE['group_id'], sot.group_id)
        self.assertEqual(EXAMPLE['stream_id'], sot.stream_id)
        self.assertEqual(EXAMPLE['stream_name'], sot.stream_name)
