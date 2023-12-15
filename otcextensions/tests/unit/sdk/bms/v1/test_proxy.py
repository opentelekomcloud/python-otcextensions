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
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.bms.v1 import _proxy


class TestBMSProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestBMSProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestExtractName(TestBMSProxy):

    def test_extract_name(self):

        self.assertEqual(
            ['flavors'],
            self.proxy._extract_name(
                '/v1/7ed5f793b8354ea9b27a849f17af4733/flavors', project_id='7ed5f793b8354ea9b27a849f17af4733')
        )
        self.assertEqual(
            ['flavors', 'detail'],
            self.proxy._extract_name(
                '/v1/7ed5f793b8354ea9b27a849f17af4733/flavors/detail', project_id='7ed5f793b8354ea9b27a849f17af4733')
        )
        self.assertEqual(
            ['limits'],
            self.proxy._extract_name(
                '/v1/7ed5f793b8354ea9b27a849f17af4733/limits', project_id='7ed5f793b8354ea9b27a849f17af4733')
        )
