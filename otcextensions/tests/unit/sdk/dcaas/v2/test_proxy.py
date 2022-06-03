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

from otcextensions.sdk.dcaas.v2 import _proxy
from otcextensions.sdk.dcaas.v2 import endpoint_group as _endpoint_group

from openstack.tests.unit import test_proxy_base


class TestDcaasProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDcaasProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)

    def test_endpoint_groups(self):
        self.verify_list(
            self.proxy.endpoint_groups,
            _endpoint_group.DirectConnectEndpointGroup
        )

    def test_endpoint_groups_query(self):
        self.verify_list(
            self.proxy.endpoint_groups,
            _endpoint_group.DirectConnectEndpointGroup,
            method_kwargs={
                'name': 'test_name',
                'description': 'test description',
                'endpoints': ['10.2.0.0/24', '10.3.0.0/24'],
                'tenant_id': '6fbe9263116a4b68818cf1edce16bc4f',
                'type': 'cidr'
            },
            expected_kwargs={
                'name': 'test_name',
                'description': 'test description',
                'endpoints': ['10.2.0.0/24', '10.3.0.0/24'],
                'tenant_id': '6fbe9263116a4b68818cf1edce16bc4f',
                'type': 'cidr'
            }
        )

    def test_create_endpoint_group(self):
        self.verify_create(
            self.proxy.create_endpoint_group,
            _endpoint_group.DirectConnectEndpointGroup,
            method_kwargs={
                'name': 'test_name',
                'tenant_id': '6fbe9263116a4b68818cf1edce16bc4f',
                'endpoints': ['10.2.0.0/24', '10.3.0.0/24'],
                'type': 'cidr'
            },
            expected_kwargs={
                'prepend_key': False,
                'name': 'test_name',
                'tenant_id': '6fbe9263116a4b68818cf1edce16bc4f',
                'endpoints': ['10.2.0.0/24', '10.3.0.0/24'],
                'type': 'cidr'
            }
        )

    def test_get_endpoint_group(self):
        self.verify_get(self.proxy.get_endpoint_group,
                        _endpoint_group.DirectConnectEndpointGroup
                        )

    def test_find_endpoint_group(self):
        self.verify_find(self.proxy.find_endpoint_group,
                        _endpoint_group.DirectConnectEndpointGroup,
                        method_kwargs = {'id': 'test_id'},
                        expected_kwargs = {'id': 'test_id'}
                         )

    def test_update_endpoint_group(self):
        self.verify_update(self.proxy.update_endpoint_group,
                           _endpoint_group.DirectConnectEndpointGroup,
                           method_kwargs={'id':'test_id'},
                           expected_kwargs={'id':'test_id'}
                           )

    def test_delete_endpoint_group(self):
        self.verify_delete(self.proxy.delete_endpoint_group,
                           _endpoint_group.DirectConnectEndpointGroup
                           )
