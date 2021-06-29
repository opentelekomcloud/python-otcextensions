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

from otcextensions.sdk.dds.v3 import flavor

EXAMPLE = {
    "region": "eu-de",
    "engine_name": "engine",
}


class TestFlavor(base.TestCase):

    def test_basic(self):
        sot = flavor.Flavor()

        self.assertEqual('/flavors', sot.base_path)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual({'limit': 'limit',
                              'marker': 'marker',
                              'region': 'region',
                              'engine_name': 'engine_name'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = flavor.Flavor(**EXAMPLE)
        self.assertEqual(EXAMPLE['region'], sot.region)
        self.assertEqual(EXAMPLE['engine_name'], sot.engine_name)
