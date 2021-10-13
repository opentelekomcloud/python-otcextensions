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


class TestLoadBalancerTags(TestElb):

    def setUp(self):
        super(TestLoadBalancerTags, self).setUp()

    def test_list_tags(self):
        query = {}
        tags = list(self.client.load_balancer_tags(
            loadbalancer='4a5539ee-4370-47f7-9b21-6f0500cd60f6',
            **query))
        self.assertGreaterEqual(len(tags), 0)
