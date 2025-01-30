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

from otcextensions.sdk.function_graph.v2 import event


EXAMPLE = {
    'name': 'event-xx',
    'content': 'eyJrIjoidiJ9'
}


class TestFunctionInvocation(base.TestCase):

    def test_basic(self):
        sot = event.Event()
        path = '/fgs/functions/%(function_urn)s/events'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = event.Event(**EXAMPLE)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['content'], sot.content)
