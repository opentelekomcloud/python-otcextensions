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
#
from openstack.tests.unit import test_proxy_base
from otcextensions.sdk.vpcep.v1 import _proxy
from otcextensions.sdk.vpcep.v1 import connection
from otcextensions.sdk.vpcep.v1 import endpoint
from otcextensions.sdk.vpcep.v1 import quota
from otcextensions.sdk.vpcep.v1 import service
from otcextensions.sdk.vpcep.v1 import whitelist


class TestVpcepProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVpcepProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestEndpointService(TestVpcepProxy):
    def test_list_services(self):
        self.verify_list(
            self.proxy.services,
            service.Service,
        )

    def test_create_service(self):
        self.verify_create(
            self.proxy.create_service,
            service.Service,
            method_kwargs={'name': 'id'},
            expected_kwargs={'name': 'id'},
        )

    def test_get_service(self):
        self.verify_get(
            self.proxy.get_service,
            service.Service,
        )

    def test_find_service(self):
        self.verify_find(
            self.proxy.find_service,
            service.Service,
        )

    def test_update_service(self):
        self.verify_update(
            self.proxy.update_service,
            service.Service,
        )

    def test_delete_service(self):
        self.verify_delete(
            self.proxy.delete_service,
            service.Service,
            True,
        )


class TestEndpoint(TestVpcepProxy):
    def test_endpoints(self):
        self.verify_list(self.proxy.endpoints, endpoint.Endpoint)

    def test_endpoint_create(self):
        self.verify_create(
            self.proxy.create_endpoint,
            endpoint.Endpoint,
            method_kwargs={'name': 'id'},
            expected_kwargs={'name': 'id'},
        )

    def test_endpoint_get(self):
        self.verify_get(self.proxy.get_endpoint, endpoint.Endpoint)

    def test_endpoint_delete(self):
        self.verify_delete(self.proxy.delete_endpoint, endpoint.Endpoint, True)


class TestWhitelist(TestVpcepProxy):
    def test_service_whitelist(self):
        self.verify_list(
            self.proxy.service_whitelist,
            whitelist.Whitelist,
            method_kwargs={'service': 'endpoint-service-id'},
            expected_kwargs={'endpoint_service_id': 'endpoint-service-id'},
        )

    def test_manage_service_whitelist_add(self):
        self._verify(
            'otcextensions.sdk.vpcep.v1.whitelist.Whitelist.add',
            self.proxy.manage_service_whitelist,
            method_kwargs={
                'service': 'endpoint-service-id',
                'action': 'add',
                'domains': ['abc', 'xyz'],
            },
            expected_args=[self.proxy, ['abc', 'xyz']],
        )

    def test_manage_service_whitelist_remove(self):
        self._verify(
            'otcextensions.sdk.vpcep.v1.whitelist.Whitelist.remove',
            self.proxy.manage_service_whitelist,
            method_kwargs={
                'service': 'endpoint-service-id',
                'action': 'remove',
                'domains': ['abc', 'xyz'],
            },
            expected_args=[self.proxy, ['abc', 'xyz']],
        )


class TestConnection(TestVpcepProxy):
    def test_service_connections(self):
        self.verify_list(
            self.proxy.service_connections,
            connection.Connection,
            method_kwargs={'service': 'endpoint-service-id'},
            expected_kwargs={'endpoint_service_id': 'endpoint-service-id'},
        )

    def test_manage_service_connections_accept(self):
        self._verify(
            'otcextensions.sdk.vpcep.v1.connection.Connection.accept',
            self.proxy.manage_service_connections,
            method_kwargs={
                'service': 'endpoint-service-id',
                'action': 'accept',
                'endpoints': ['abc', 'xyz'],
            },
            expected_args=[self.proxy, ['abc', 'xyz']],
        )

    def test_manage_service_connections_reject(self):
        self._verify(
            'otcextensions.sdk.vpcep.v1.connection.Connection.reject',
            self.proxy.manage_service_connections,
            method_kwargs={
                'service': 'endpoint-service-id',
                'action': 'reject',
                'endpoints': ['abc', 'xyz'],
            },
            expected_args=[self.proxy, ['abc', 'xyz']],
        )


class TestQuota(TestVpcepProxy):
    def test_resource_quota(self):
        self.verify_list(self.proxy.resource_quota, quota.Quota)
