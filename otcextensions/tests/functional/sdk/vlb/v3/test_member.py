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


class TestMember(TestVlb):

    def setUp(self):
        super(TestMember, self).setUp()
        self.create_network()
        self.create_server()
        self.create_load_balancer()
        self.create_listener()
        self.create_pool()
        self.create_member()

    def test_01_list_members(self):
        members = list(self.client.members(TestVlb.pool))
        self.assertGreaterEqual(len(members), 0)

    def test_02_get_member(self):
        member = self.client.get_member(TestVlb.member, TestVlb.pool)
        self.assertIsNotNone(member)

    def test_03_find_member(self):
        member = self.client.find_member(TestVlb.member.name, TestVlb.pool)
        self.assertIsNotNone(member)

    def test_04_update_member(self):
        new_weight = 20
        member = self.client.update_member(
            TestVlb.member,
            TestVlb.pool,
            weight=new_weight,
        )
        self.assertEqual(member['weight'], new_weight)

        # cleanup
        self.client.delete_member(
            TestVlb.member,
            TestVlb.pool
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
        self.delete_server()
        self.ecs_client.delete_keypair(TestVlb.keypair)

        self.addCleanup(self.destroy_network, TestVlb.network)
