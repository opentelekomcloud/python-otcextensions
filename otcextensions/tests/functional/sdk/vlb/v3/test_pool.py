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


class TestPool(TestVlb):

    def setUp(self):
        super(TestPool, self).setUp()
        self.create_network()
        self.create_load_balancer()
        self.create_listener()
        self.create_pool()

    def test_01_list_pools(self):
        pools = list(self.client.pools(name=TestVlb.pool.name))
        self.assertGreaterEqual(len(pools), 0)

    def test_02_get_pool(self):
        pool = self.client.get_pool(TestVlb.pool)
        self.assertIsNotNone(pool)

    def test_03_find_pool(self):
        pool = self.client.find_pool(TestVlb.pool.name)
        self.assertIsNotNone(pool)

    def test_04_update_pool(self):
        new_description = 'changed'
        lb_algorithm = 'LEAST_CONNECTIONS'
        pool = self.client.update_pool(
            TestVlb.pool,
            description=new_description,
            lb_algorithm=lb_algorithm
        )
        self.assertEqual(pool['description'], new_description)
        self.assertEqual(pool['lb_algorithm'], lb_algorithm)

        # cleanup
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
