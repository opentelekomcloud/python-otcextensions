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
from otcextensions.sdk.apig.v2 import tag

EXAMPLE_TAG = {
    'tags': ['env:prod', 'team:backend'],
    'size': 2,
    'total': 10
}


class TestTag(base.TestCase):

    def test_basic(self):
        sot = tag.Tag()
        self.assertEqual('apigw/instances/%(gateway_id)s/tags', sot.base_path)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = tag.Tag(**EXAMPLE_TAG)
        self.assertEqual(['env:prod', 'team:backend'], sot.tags)
        self.assertEqual(2, sot.size)
        self.assertEqual(10, sot.total)
