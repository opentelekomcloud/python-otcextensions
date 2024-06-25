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
import uuid

from openstack.tests.unit import base
from otcextensions.sdk.dws.v1 import flavor

EXAMPLE = {
    'id': uuid.uuid4().hex,
    'detail': [
        {'value': '32', 'type': 'vCPU'},
        {'value': '4000', 'type': 'SSD', 'unit': 'GB'},
        {'value': '256', 'type': 'mem', 'unit': 'GB'},
        {'value': 'eu-de-02,eu-de-01', 'type': 'availableZones'},
    ],
    'spec_name': 'dws2.m6.8xlarge.8',
    'vCPU': '32',
    'disk_type': 'SSD',
    'disk_size': '4000',
    'mem': '256',
    'availableZones': 'eu-de-02,eu-de-01',
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
        self.assertEqual(EXAMPLE['availableZones'], sot.availability_zones)
        self.assertEqual(EXAMPLE['detail'], sot.detail)
        self.assertEqual(EXAMPLE['disk_type'], sot.disk_type)
        self.assertEqual(int(EXAMPLE['disk_size']), sot.disk_size)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(int(EXAMPLE['mem']), sot.ram)
        self.assertEqual(EXAMPLE['spec_name'], sot.name)
        self.assertEqual(EXAMPLE['spec_name'], sot.spec_name)
        self.assertEqual(int(EXAMPLE['vCPU']), sot.vcpu)
