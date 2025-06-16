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

from otcextensions.tests.functional.sdk.apig import TestApiG


class TestApiCall(TestApiG):
    gateway = '560de602c9f74969a05ff01d401a53ed'

    def setUp(self):
        super(TestApiCall, self).setUp()

    def tearDown(self):
        super(TestApiCall, self).tearDown()

    def test_get_api_call_for_period(self):
        attrs = {
            'api_id': '64182cc7e77245ebbae8cf3b8522a540',
            'duration': '1h',
        }
        found = self.client.list_api_calls_for_period(gateway=self.gateway,
                                                      **attrs)
        self.assertIsNotNone(found)

    def test_get_api_call_for_group(self):
        attrs = {
            'group_id': 'ce973ff83ce54ef192c80bde884aa0ac',
        }
        found = self.client.list_api_calls_for_group(gateway=self.gateway,
                                                     **attrs)
        self.assertIsNotNone(found)

    def test_list_metric_data(self):
        attrs = {
            'dim': 'inbound_eip',
            'metric_name': 'upstream_bandwidth',
            'from': '1740787200000',
            'to': '1740873600000',
            'period': 3600,
            'filter': 'average',
        }
        found = self.client.list_metric_data(gateway=self.gateway, **attrs)
        self.assertIsNotNone(found)
        self.assertGreater(len(found), 0)
