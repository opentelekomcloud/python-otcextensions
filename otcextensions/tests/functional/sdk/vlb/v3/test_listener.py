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


class TestListener(TestVlb):

    def setUp(self):
        super(TestListener, self).setUp()
        self.create_network()
        self.create_load_balancer()
        self.create_listener()

    def test_01_list_listeners(self):
        lst = list(self.client.listeners())
        self.assertIsNotNone(lst)

    def test_02_get_listener(self):
        lst = self.client.get_listener(TestVlb.listener)
        self.assertIsNotNone(lst)

    def test_03_find_listener(self):
        lst = self.client.find_listener(TestVlb.listener.name)
        self.assertIsNotNone(lst)

    def test_05_update_listener(self):
        new_description = 'changed'
        lst = self.client.update_listener(
            TestVlb.listener,
            description=new_description
        )
        self.assertEqual(lst['description'], new_description)

        # cleanup
        self.client.delete_listener(
            TestVlb.listener
        )
        self.client.delete_load_balancer(
            TestVlb.load_balancer
        )
        self.net_client.delete_ip(
            TestVlb.load_balancer.floating_ips[0]['publicip_id']
        )
        self.addCleanup(self.destroy_network, TestVlb.network)
