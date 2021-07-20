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


class TestLoadbalancer(TestVlb):

    def setUp(self):
        super(TestLoadbalancer, self).setUp()
        self.create_network()
        self.create_load_balancer()

    def test_01_list_loadbalancers(self):
        elbs = list(self.client.load_balancers())
        self.assertIsNotNone(elbs)

    def test_02_get_loadbalancer(self):
        elb = self.client.get_load_balancer(TestVlb.load_balancer)
        self.assertIsNotNone(elb)

    def test_03_find_loadbalancer(self):
        elb = self.client.find_load_balancer(TestVlb.load_balancer.name)
        self.assertIsNotNone(elb)

    def test_04_get_loadbalancer_statuses(self):
        elb = self.client.get_load_balancer_statuses(TestVlb.load_balancer.id)
        self.assertIsNotNone(elb)

    def test_05_update_loadbalancer(self):
        new_description = 'changed'
        elb = self.client.update_load_balancer(
            TestVlb.load_balancer,
            description=new_description
        )
        self.assertEqual(elb['description'], new_description)

        # cleanup
        self.client.delete_load_balancer(
            TestVlb.load_balancer
        )
        self.net_client.delete_ip(
            elb['floating_ips'][0]['publicip_id']
        )
        self.addCleanup(self.destroy_network, TestVlb.network)
