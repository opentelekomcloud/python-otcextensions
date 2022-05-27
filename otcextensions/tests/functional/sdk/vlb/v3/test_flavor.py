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

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestFlavor(TestVlb):

    def setUp(self):
        super(TestFlavor, self).setUp()

    def test_list_flavors(self):
        flavor_name = 'L4_flavor.elb.s2.medium'
        flavors = list(self.client.flavors())
        self.assertGreaterEqual(len(flavors), 0)
        flavor = list(self.client.flavors(name=flavor_name))
        self.assertEqual(flavor[0].name, flavor_name)

    def test_get_flavor(self):
        flavor_name = 'L4_flavor.elb.s2.medium'
        flavors = list(self.client.flavors(name=flavor_name))
        flavor = self.client.get_flavor(flavors[0])
        self.assertEqual(flavor.name, flavor_name)

    def test_find_flavor(self):
        flavor_name = 'L4_flavor.elb.s2.medium'
        flavor = self.client.find_flavor(flavor_name)
        self.assertEqual(flavor.name, flavor_name)
