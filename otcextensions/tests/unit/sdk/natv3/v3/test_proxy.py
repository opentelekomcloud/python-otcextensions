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
from otcextensions.sdk.natv3.v3 import _proxy
from otcextensions.sdk.natv3.v3 import gateway as _gateway


class TestNatProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestNatProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestNatGateway(TestNatProxy):
    def test_gateways(self):
        self.verify_list(self.proxy.gateways, _gateway.Gateway)
