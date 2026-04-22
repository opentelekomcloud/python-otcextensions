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
from otcextensions.sdk.natv3.v3 import dnat
from otcextensions.sdk.natv3.v3 import gateway
from otcextensions.sdk.natv3.v3 import snat
from otcextensions.sdk.natv3.v3 import transit_ip


class TestNatv3Proxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestNatv3Proxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestPrivateNatGateway(TestNatv3Proxy):

    def test_private_nat_gateways(self):
        self.verify_list(self.proxy.private_nat_gateways, gateway.PrivateNatGateway)

    def test_get_private_nat_gateway(self):
        self.verify_get(self.proxy.get_private_nat_gateway, gateway.PrivateNatGateway)

    def test_create_private_nat_gateway(self):
        self.verify_create(
            self.proxy.create_private_nat_gateway, gateway.PrivateNatGateway
        )

    def test_update_private_nat_gateway(self):
        self.verify_update(
            self.proxy.update_private_nat_gateway, gateway.PrivateNatGateway
        )

    def test_delete_private_nat_gateway(self):
        self.verify_delete(
            self.proxy.delete_private_nat_gateway, gateway.PrivateNatGateway
        )


class TestPrivateDnat(TestNatv3Proxy):

    def test_private_dnat_rules(self):
        self.verify_list(self.proxy.private_dnat_rules, dnat.PrivateDnat)

    def test_create_private_dnat_rule(self):
        self.verify_create(self.proxy.create_private_dnat_rule, dnat.PrivateDnat)

    def test_get_private_dnat_rule(self):
        self.verify_get(self.proxy.get_private_dnat_rule, dnat.PrivateDnat)

    def test_update_private_dnat_rule(self):
        self.verify_update(self.proxy.update_private_dnat_rule, dnat.PrivateDnat)

    def test_delete_private_dnat_rule(self):
        self.verify_delete(self.proxy.delete_private_dnat_rule, dnat.PrivateDnat)


class TestPrivateSnat(TestNatv3Proxy):

    def test_private_snat_rules(self):
        self.verify_list(self.proxy.private_snat_rules, snat.PrivateSnat)

    def test_get_private_snat_rule(self):
        self.verify_get(self.proxy.get_private_snat_rule, snat.PrivateSnat)

    def test_create_private_snat_rule(self):
        self.verify_create(self.proxy.create_private_snat_rule, snat.PrivateSnat)

    def test_update_private_snat_rule(self):
        self.verify_update(self.proxy.update_private_snat_rule, snat.PrivateSnat)

    def test_delete_private_snat_rule(self):
        self.verify_delete(self.proxy.delete_private_snat_rule, snat.PrivateSnat)


class TestPrivateTransitIp(TestNatv3Proxy):

    def test_private_transit_ips(self):
        self.verify_list(self.proxy.private_transit_ips, transit_ip.PrivateTransitIp)

    def test_get_private_transit_ip(self):
        self.verify_get(self.proxy.get_private_transit_ip, transit_ip.PrivateTransitIp)
