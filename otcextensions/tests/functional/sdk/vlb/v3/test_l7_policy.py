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

from otcextensions.tests.functional.sdk.vlb import TestVlb


class TestL7Policy(TestVlb):
    uuid_v4 = uuid.uuid4().hex[:8]

    def setUp(self):
        super(TestL7Policy, self).setUp()
        self.create_network()
        self.create_load_balancer()
        self.create_listener(protocol='HTTP')
        self.create_certificate()
        self.create_listener(
            protocol_port=443,
            protocol='HTTPS',
            name='sdk-vlb-test-r-lis-' + self.uuid_v4,
            additional=True,
            default_tls_container_ref=TestVlb.certificate.id)
        self.create_l7policy(TestVlb.additional_listener.id)

    def test_01_list_l7Policies(self):
        l7p = list(self.client.l7_policies())
        self.assertGreaterEqual(len(l7p), 0)

    def test_02_get_l7Policy(self):
        l7p = self.client.get_l7_policy(TestVlb.l7policy)
        self.assertIsNotNone(l7p)

    def test_03_find_l7Policy(self):
        l7p = self.client.find_l7_policy(TestVlb.l7policy.name)
        self.assertIsNotNone(l7p)

    def test_04_update_l7Policy(self):
        description = 'updated_policy'
        l7p = self.client.update_l7_policy(
            TestVlb.l7policy,
            description=description,
        )
        self.assertEqual(l7p['description'], description)

        # cleanup
        self.client.delete_l7_policy(TestVlb.l7policy)
        self.client.delete_listener(TestVlb.additional_listener)
        self.client.delete_listener(TestVlb.listener)
        self.client.delete_certificate(TestVlb.certificate)
        self.client.delete_load_balancer(TestVlb.load_balancer)
        self.net_client.delete_ip(
            TestVlb.load_balancer.floating_ips[0]['publicip_id']
        )

        self.addCleanup(self.destroy_network, TestVlb.network)
