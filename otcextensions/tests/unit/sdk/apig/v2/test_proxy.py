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
from otcextensions.sdk.apig.v2 import _proxy
from otcextensions.sdk.apig.v2 import gateway as _gateway
from otcextensions.sdk.apig.v2 import az as _az
from openstack.tests.unit import test_proxy_base
from unittest import mock


class TestApiGatewayProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestApiGatewayProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestApiGatewayFunctions(TestApiGatewayProxy):
    def test_gateways(self):
        self.verify_list(self.proxy.gateways, _gateway.Gateway)

    def test_azs(self):
        self.verify_list(self.proxy.azs, _az.AZ)

    def test_create_gateway(self):
        self.verify_create(self.proxy.create_gateway,
                           _gateway.Gateway)

    def test_delete_gateway(self):
        gateway = _gateway.Gateway()
        self.verify_delete(self.proxy.delete_gateway,
                           _gateway.Gateway,
                           method_args=[gateway],
                           expected_args=[gateway]
                           )

    def test_get_gateway(self):
        self.verify_get(self.proxy.get_gateway,
                        _gateway.Gateway)

    def test_update_gateway(self):
        self.verify_update(self.proxy.update_gateway,
                           _gateway.Gateway)

    def test_get_gateway_progress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._get_creation_progress',
            self.proxy.get_gateway_progress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_modify_spec(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._modify_spec',
            self.proxy.modify_gateway_spec,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_get_constraints(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._get_constraints',
            self.proxy.get_constraints,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_enable_public_access(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._enable_public_access',
            self.proxy.enable_public_access,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_update_public_access(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._update_public_access',
            self.proxy.update_public_access,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_disable_public_access(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._disable_public_access',
            self.proxy.disable_public_access,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_bind_eip(self):
        gateway = _gateway.Gateway()
        self.proxy._get_resource = mock.Mock(return_value=gateway)
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._bind_eip',
            self.proxy.bind_eip,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_unbind_eip(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._unbind_eip',
            self.proxy.unbind_eip,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_enable_ingress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._enable_ingress',
            self.proxy.enable_ingress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_update_ingress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._update_ingress',
            self.proxy.update_ingress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )

    def test_disable_ingress(self):
        gateway = _gateway.Gateway()
        self._verify(
            'otcextensions.sdk.apig.v2.gateway.'
            'Gateway._disable_ingress',
            self.proxy.disable_ingress,
            method_args=[gateway],
            expected_args=[self.proxy, gateway]
        )
