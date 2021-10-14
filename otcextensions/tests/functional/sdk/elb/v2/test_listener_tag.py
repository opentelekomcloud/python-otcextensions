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


from otcextensions.tests.functional.sdk.elb import TestElb


class TestLoadBalancerListenerTags(TestElb):

    def setUp(self):
        super(TestLoadBalancerListenerTags, self).setUp()
        self.create_network()
        self.create_load_balancer()
        self.create_listener()

    def test_01_list_tags(self):
        query = {}
        tags = list(self.client.listener_tags(
            listener='6d565cb7-2be4-4fcc-80c6-cc10765317a5',
            **query))
        self.assertGreaterEqual(len(tags), 0)

    def test_02_create_tag(self):
        kv = {
            'key': 'key1',
            'value': 'value1'
        }
        tag = self.client.create_listener_tag(
            listener='6d565cb7-2be4-4fcc-80c6-cc10765317a5',
            **kv)
        self.assertIsNotNone(tag)
        self.assertEqual(kv['key'], tag.key)
        self.assertEqual(kv['value'], tag.value)

    def test_03_delete_tag(self):
        key = 'key1'
        tag = self.client.delete_listener_tag(
            listener='6d565cb7-2be4-4fcc-80c6-cc10765317a5',
            key=key
        )
        self.assertIsNotNone(tag)

        self.client.delete_listener(
            TestElb.listener
        )
        self.client.delete_load_balancer(
            TestElb.load_balancer
        )
        self.addCleanup(self.destroy_network, TestElb.network)
