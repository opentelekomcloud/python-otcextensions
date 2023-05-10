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


class TestIpAddressGroup(TestVlb):

    def setUp(self):
        super(TestIpAddressGroup, self).setUp()
        self.create_ip_address_group()

    def test_01_list_ip_address_groups(self):
        ip_groups = list(self.client.ip_address_groups(
            name=TestIpAddressGroup.ip_address_group.name))
        self.assertGreaterEqual(len(ip_groups), 0)

    def test_02_get_ip_address_group(self):
        ip_address_group = self.client.get_ip_address_group(
            TestVlb.ip_address_group)
        self.assertIsNotNone(ip_address_group)

    def test_03_find_ip_address_group(self):
        ip_address_group = self.client.find_ip_address_group(
            TestVlb.ip_address_group.name)
        self.assertIsNotNone(ip_address_group)

    def test_04_update_ip_address_group(self):
        new_description = 'changed'
        ip_list = [{"ip": "192.168.1.125", "description": ""}]
        ip_address_group = self.client.update_ip_address_group(
            TestVlb.ip_address_group,
            description=new_description,
            ip_list=ip_list
        )
        self.assertEqual(ip_address_group['description'], new_description)
        self.assertEqual(ip_address_group['ip_list'], ip_list)

        # cleanup
        self.client.delete_ip_address_group(
            TestVlb.ip_address_group
        )
