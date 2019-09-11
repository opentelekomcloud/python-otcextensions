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

from otcextensions.sdk.rds.v3 import flavor 

EXAMPLE = {
    "vcpus": "1",
    "ram": 2,
    "spec_code": "rds.mysql.c2.medium.ha",
    "instance_mode": "ha"
}

class TestFlavor(base.TestCase):

    def setUp(self):
        super(TestFlavor, self).setUp()

    def test_basic(self):
        sot = flavor.Flavor()

        self.assertEqual('/flavors/%(datastore_name)s', sot.base_path)
        self.assertEqual('flavors', sot.resources_key)
        self.assertIsNone(sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertDictEqual({'limit': 'limit', 'marker': 'marker', 'version_name': 'version_name'}, sot._query_mapping._mapping)

    def test_make_it(self):

        sot = flavor.Flavor(**EXAMPLE)
        self.assertEqual(EXAMPLE['spec_code'], sot.spec_code)
        self.assertEqual(EXAMPLE['vcpus'], sot.vcpus)
        self.assertEqual(EXAMPLE['ram'], sot.ram)
        self.assertEqual(EXAMPLE['instance_mode'], sot.instance_mode)
