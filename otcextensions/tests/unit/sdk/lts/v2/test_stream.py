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

from otcextensions.sdk.lts.v2 import stream

EXAMPLE = {
    'id': 'id',
    'creation_time': 'creation-time',
    'name': 'name',
    'log_group_id': 'log_group_id',
    'filter_count': 5,
    'tag': 'tag',
}


class TestStream(base.TestCase):

    def test_basic(self):
        sot = stream.Stream()
        path = '/groups/%(log_group_id)s/streams'
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = stream.Stream(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['creation_time'], sot.creation_time)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['log_group_id'], sot.log_group_id)
        self.assertEqual(EXAMPLE['filter_count'], sot.filter_count)
        self.assertEqual(EXAMPLE['tag'], sot.tag)
