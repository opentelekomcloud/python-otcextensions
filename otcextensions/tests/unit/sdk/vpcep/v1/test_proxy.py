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

from otcextensions.sdk.vpcep.v1 import _proxy
from otcextensions.sdk.vpcep.v1 import endpoint_service as _endpoint_service
from otcextensions.sdk.vpcep.v1 import endpoint as _endpoint

from openstack.tests.unit import test_proxy_base


class TestVpcepProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVpcepProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestEndpointService(TestVpcepProxy):
    def test_create_endpoint_service(self):
        self.verify_create(self.proxy.create_endpoint_service,
                           _endpoint_service.EndpointService,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_delete_endpoint_service(self):
        self.verify_delete(self.proxy.delete_endpoint_service,
                           _endpoint_service.EndpointService, True)

    def test_get_endpoint_service(self):
        self.verify_get(self.proxy.get_endpoint_service,
                        _endpoint_service.EndpointService)

    def test_list_endpoint_services(self):
        self.verify_list(self.proxy.endpoint_services,
                         _endpoint_service.EndpointService)

    def test_update_endpoint_service(self):
        self.verify_update(self.proxy.update_endpoint_service,
                           _endpoint_service.EndpointService)

    def test_list_whitelist(self):
        self.verify_list(self.proxy.whitelist,
                         _endpoint_service.Whitelist,
                         method_kwargs={'endpoint_service': 'uuid'},
                         expected_kwargs={'endpoint_service_id': 'uuid'}
                         )

    def test_manage_whitelist(self):
        self._verify(
            ('otcextensions.sdk.vpcep.v1.endpoint_service.'
             'Whitelist._manage_whitelist'),
            self.proxy.manage_whitelist,
            method_args=[
                _endpoint_service.Whitelist,
                'domain-uuid',
                'add'
            ],
            expected_args=[
                self.proxy,
                'domain-uuid',
                'add'
            ],
        )

    def test_list_connections(self):
        self.verify_list(self.proxy.connections,
                         _endpoint_service.Connection,
                         method_kwargs={'endpoint_service': 'uuid'},
                         expected_kwargs={'endpoint_service_id': 'uuid'}
                         )

    def test_manage_connection(self):
        self._verify(
            ('otcextensions.sdk.vpcep.v1.endpoint_service.'
             'Connection._manage_connection'),
            self.proxy.manage_connection,
            method_args=[
                _endpoint_service.Connection,
                'endpoint-uuid1,endpoint-uuid2',
                'receive'
            ],
            expected_args=[
                self.proxy,
                'endpoint-uuid1,endpoint-uuid2',
                'receive'
            ],
        )


class TestEndpoint(TestVpcepProxy):
    def test_endpoint_create(self):
        self.verify_create(self.proxy.create_endpoint,
                           _endpoint.Endpoint,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_endpoint_delete(self):
        self.verify_delete(self.proxy.delete_endpoint,
                           _endpoint.Endpoint, True)

    def test_endpoint_get(self):
        self.verify_get(self.proxy.get_endpoint,
                        _endpoint.Endpoint)

    def test_endpoints(self):
        self.verify_list(self.proxy.endpoints,
                         _endpoint.Endpoint)
