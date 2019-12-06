<<<<<<< Updated upstream
=======
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

from otcextensions.sdk.nat.v2 import _proxy
from otcextensions.sdk.nat.v2 import snat
from otcextensions.sdk.nat.v2 import dnat
from otcextensions.sdk.nat.v2 import gateway

from openstack.tests.unit import test_proxy_base


class TestNatProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestNatProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestNatGateway(TestNatProxy):
    def test_gateway_create(self):
        self.verify_create(self.proxy.create_gateway, gateway.Gateway,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_gateway_delete(self):
        self.verify_delete(self.proxy.delete_gateway,
                           gateway.Gateway, True)

    def test_gateway_get(self):
        self.verify_get(self.proxy.get_gateway, gateway.Gateway)

    def test_gateways(self):
        self.verify_list(self.proxy.gateways, gateway.Gateway)

    def test_gateway_update(self):
        self.verify_update(self.proxy.update_gateway, gateway.Gateway)


class TestNatSnatRule(TestNatProxy):
    def test_snat_rule_create(self):
        self.verify_create(self.proxy.create_snat_rule, snat.Snat,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_snat_rule_delete(self):
        self.verify_delete(self.proxy.delete_snat_rule,
                           snat.Snat, True)

    def test_snat_rule_get(self):
        self.verify_get(self.proxy.get_snat_rule, snat.Snat)

    def test_snat_rules(self):
        self.verify_list(self.proxy.snat_rules, snat.Snat)


class TestNatDnatRule(TestNatProxy):
    def test_dnat_rule_create(self):
        self.verify_create(self.proxy.create_dnat_rule, dnat.Dnat,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_dnat_rule_delete(self):
        self.verify_delete(self.proxy.delete_dnat_rule,
                           dnat.Dnat, True)

    def test_dnat_rule_get(self):
        self.verify_get(self.proxy.get_dnat_rule, dnat.Dnat)
# move
    def test_dnat_rules(self):
        self.verify_list(self.proxy.dnat_rules, dnat.Dnat)
>>>>>>> Stashed changes
