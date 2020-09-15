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
from otcextensions.sdk.vpcep.v1 import endpoint_service
from otcextensions.sdk.vpcep.v1 import endpoint

from openstack.tests.unit import test_proxy_base


class TestVpcepProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVpcepProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestEndpointService(TestVpcepProxy):
    def test_endpoint_service_create(self):
        self.verify_create(self.proxy.create_endpoint_service,
                           endpoint_service.EndpointService,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_endpoint_service_delete(self):
        self.verify_delete(self.proxy.delete_endpoint_service,
                           endpoint_service.EndpointService, True)

    def test_endpoint_service_get(self):
        self.verify_get(self.proxy.get_endpoint_service,
                        endpoint_service.EndpointService)

    def test_endpoint_services(self):
        self.verify_list(self.proxy.endpoint_services,
                         endpoint_service.EndpointService)

    def test_endpoint_service_update(self):
        self.verify_update(self.proxy.update_endpoint_service,
                           endpoint_service.EndpointService)

    def test_endpoint_service_whitelists(self):
        self.verify_list(self.proxy.list_endpoint_service_whitelist,
                         endpoint_service.Whitelist,
                         method_kwargs={'endpoint_service': 'uuid'},
                         expected_kwargs={'endpoint_service_id': 'uuid'}
                         )

    def test_endpoint_service_whitelists_manage(self):
        self.verify_create(self.proxy.manage_endpoint_service_whitelist,
                           endpoint_service.ManageWhitelist,
                           method_kwargs={
                               'endpoint_service': 'uuid',
                               'domains': ['uuid1'],
                               'action': 'add'},
                           expected_kwargs={
                               'endpoint_service_id': 'uuid',
                               'permissions': ['iam:domain::uuid1'],
                               'action': 'add'}
                           )

    def test_endpoint_service_connections(self):
        self.verify_list(self.proxy.list_endpoint_service_connection,
                         endpoint_service.Connection,
                         method_kwargs={'endpoint_service': 'uuid'},
                         expected_kwargs={'endpoint_service_id': 'uuid'}
                         )

    def test_endpoint_service_connections_manage(self):
        self.verify_create(self.proxy.manage_endpoint_service_connection,
                           endpoint_service.ManageConnection,
                           method_kwargs={
                               'endpoint_service': 'uuid',
                               'endpoints': ['uuid1', 'uuid2'],
                               'action': 'reject'},
                           expected_kwargs={
                               'endpoint_service_id': 'uuid',
                               'endpoints': ['uuid1', 'uuid2'],
                               'action': 'reject'}
                           )


class TestEndpoint(TestVpcepProxy):
    def test_endpoint_create(self):
        self.verify_create(self.proxy.create_endpoint,
                           endpoint.Endpoint,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_endpoint_delete(self):
        self.verify_delete(self.proxy.delete_endpoint,
                           endpoint.Endpoint, True)

    def test_endpoint_get(self):
        self.verify_get(self.proxy.get_endpoint,
                        endpoint.Endpoint)

    def test_endpoints(self):
        self.verify_list(self.proxy.endpoints,
                         endpoint.Endpoint)
