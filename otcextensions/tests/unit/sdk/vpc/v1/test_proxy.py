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
from otcextensions.sdk.vpc.v1 import _proxy
from otcextensions.sdk.vpc.v1 import peering
from otcextensions.sdk.vpc.v1 import route
from otcextensions.sdk.vpc.v1 import vpc

from openstack.tests.unit import test_proxy_base


class TestVpcProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVpcProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestVpcPeering(TestVpcProxy):
    def test_peering_create(self):
        self.verify_create(self.proxy.create_peering, peering.Peering,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_peering_delete(self):
        self.verify_delete(self.proxy.delete_peering,
                           peering.Peering, True)

    def test_peering_get(self):
        self.verify_get(self.proxy.get_peering, peering.Peering)

    def test_peerings(self):
        self.verify_list(self.proxy.peerings, peering.Peering)

    def test_peering_update(self):
        self.verify_update(self.proxy.update_peering, peering.Peering)

    def test_set_peering(self):
        self._verify(
            'otcextensions.sdk.vpc.v1.peering.Peering._set_peering',
            self.proxy.set_peering,
            method_args=[peering.Peering],
            method_kwargs={'set_status': 'accept'},
            expected_args=[self.proxy, 'accept']
        )


class TestVpcRoute(TestVpcProxy):
    def test_route_add(self):
        self.verify_create(self.proxy.add_route, route.Route,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_route_delete(self):
        self.verify_delete(self.proxy.delete_route,
                           route.Route, True)

    def test_route_get(self):
        self.verify_get(self.proxy.get_route, route.Route)

    def test_routes(self):
        self.verify_list(self.proxy.routes, route.Route)


class TestVpc(TestVpcProxy):
    def test_vpc_create(self):
        self.verify_create(self.proxy.create_vpc, vpc.Vpc,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={
                               'name': 'id',
                               'project_id': self.proxy.get_project_id()
                           })

    def test_vpc_delete(self):
        self.verify_delete(self.proxy.delete_vpc, vpc.Vpc, True,
                           expected_kwargs={
                               'ignore_missing': True,
                               'project_id': self.proxy.get_project_id()})

    def test_vpc_get(self):
        self.verify_get(self.proxy.get_vpc, vpc.Vpc, 'id',
                        expected_kwargs={
                            'project_id': self.proxy.get_project_id()})

    def test_vpcs(self):
        self.verify_list(self.proxy.vpcs, vpc.Vpc,
                         expected_kwargs={
                             'project_id': self.proxy.get_project_id()
                         })

    def test_vpc_update(self):
        self.verify_update(self.proxy.update_vpc, vpc.Vpc,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={
                               'name': 'id',
                               'project_id': self.proxy.get_project_id()
                           })
