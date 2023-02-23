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
from otcextensions.sdk.dws.v1 import flavor


EXAMPLE = {
    "id": "uuid.uuid4().hex",
    "spec_name": "dws.test.flavor",
    "detail": [
        {
            "value": "4",
            "type": "vCPU"
        },
        {
            "value": "160",
            "type": "SSD",
            "unit": "GB"
        },
        {
            "value": "eu-de-01,eu-de-02",
            "type": "availableZones"
        },
        {
            "value": "32",
            "type": "mem",
            "unit": "GB"
        }
    ]
}


class TestFlavor(base.TestCase):

    def setUp(self):
        super(TestFlavor, self).setUp()

    def test_basic(self):
        sot = flavor.Flavor()

        self.assertEqual('/node-types', sot.base_path)
        self.assertEqual('node_types', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = flavor.Flavor(**EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['spec_name'], sot.name)
        self.assertEqual(EXAMPLE['spec_name'], sot.spec_name)
        # self.assertEqual(EXAMPLE['detail'], sot.detail)

        for detail in EXAMPLE['detail']:
            sot = flavor.FlavorDetail(**detail)
            self.assertEqual(detail['type'], sot.type)
            self.assertEqual(detail['value'], sot.value)
            self.assertEqual(detail.get('unit'), sot.unit)
