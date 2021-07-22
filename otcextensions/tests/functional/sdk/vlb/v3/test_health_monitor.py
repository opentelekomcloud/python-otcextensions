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


class TestHealthMonitor(TestVlb):

    def setUp(self):
        super(TestHealthMonitor, self).setUp()
        self.create_network()
        self.create_load_balancer()
        self.create_listener()
        self.create_pool()
        self.create_health_monitor()

    def test_01_list_health_monitors(self):
        hms = list(self.client.health_monitors())
        self.assertGreaterEqual(len(hms), 0)

    def test_02_get_health_monitor(self):
        hm = self.client.get_health_monitor(TestVlb.health_monitor)
        self.assertIsNotNone(hm)

    def test_03_find_health_monitor(self):
        hm = self.client.find_health_monitor(TestVlb.health_monitor.id)
        self.assertIsNotNone(hm)

    def test_04_update_health_monitor(self):
        new_delay = 20
        hm = self.client.update_health_monitor(
            TestVlb.health_monitor,
            delay=new_delay,
        )
        self.assertEqual(hm['delay'], new_delay)

        # cleanup
        self.client.delete_health_monitor(
            TestVlb.health_monitor
        )
        self.client.delete_pool(
            TestVlb.pool
        )
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
