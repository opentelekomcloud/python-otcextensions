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

from otcextensions.sdk.vpc.v1 import _proxy
from otcextensions.sdk.vpc.v1 import bandwidth as _bandwidth
from otcextensions.sdk.vpc.v1 import peering
from otcextensions.sdk.vpc.v1 import route
from otcextensions.sdk.vpc.v1 import subnet
from otcextensions.sdk.vpc.v1 import vpc


class TestVpcProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestVpcProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestVPCBandwidth(TestVpcProxy):

    # ======== Bandwidth ========
    def assign_bandwidth(self, **attrs):
        """Assign bandwidth

        :param dict attrs: Keyword arguments which will be used to assign
            a :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
        """
        project_id = self.get_project_id()
        return self._create(_bandwidth.Bandwidth,
                            project_id=project_id, **attrs)

    def add_eip_to_bandwidth(self, bandwidth, publicip_info):
        """Add an EIP to a shared bandwidth.

        :param bandwidth: The value can be the ID of a bandwidth
             or a :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
             instance.
        :param publicip_info: List from dictionaries.
        """
        bandwidth = self._get_resource(_bandwidth.Bandwidth, bandwidth)
        return bandwidth.add_eip_to_bandwidth(self, publicip_info,
                                              project_id=self.get_project_id())

    def remove_eip_from_bandwidth(self, bandwidth, **attrs):
        """Add an EIP to a shared bandwidth.

        :param bandwidth: The value can be the ID of a bandwidth
             or a :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
             instance.
        :param attrs:
        """
        bandwidth = self._get_resource(_bandwidth.Bandwidth, bandwidth)
        attrs['project_id'] = self.get_project_id()
        return bandwidth.remove_eip_from_bandwidth(
            self, **attrs)

    def delete_bandwidth(self, bandwidth, ignore_missing=True):
        """Delete a bandwidth

        :param bandwidth: key id or an instance of
            :class:`~otcextensions.sdk.vpc.v1.bandwidth.Bandwidth`
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised when
            the vpc peering does not exist.
            When set to ``True``, no exception will be set when attempting to
            delete a nonexistent peering.

        :returns: ``None``
        """
        return self._delete(
            _bandwidth.Bandwidth, bandwidth,
            ignore_missing=ignore_missing, project_id=self.get_project_id())


class TestVpcPeering(TestVpcProxy):
    def test_peering_create(self):
        self.verify_create(self.proxy.create_peering, peering.Peering,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={'name': 'id'})

    def test_peering_delete(self):
        self.verify_delete(
            self.proxy.delete_peering,
            peering.Peering, True,
            mock_method='otcextensions.sdk.vpc.v1._proxy.Proxy._delete',
        )

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
        self.verify_delete(
            self.proxy.delete_route,
            route.Route, True,
            mock_method='otcextensions.sdk.vpc.v1._proxy.Proxy._delete',
        )

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
        self.verify_delete(
            self.proxy.delete_vpc, vpc.Vpc, True,
            mock_method='otcextensions.sdk.vpc.v1._proxy.Proxy._delete',
            expected_kwargs={
                'ignore_missing': True,
                'project_id': self.proxy.get_project_id()
            })

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

    def test_vpc_find(self):
        self.verify_find(self.proxy.find_vpc, vpc.Vpc, 'id',
                         expected_kwargs={
                             'project_id': self.proxy.get_project_id()
                         })


class TestSubnet(TestVpcProxy):
    def test_subnet_create(self):
        self.verify_create(self.proxy.create_subnet, subnet.Subnet,
                           method_kwargs={'name': 'id'},
                           expected_kwargs={
                               'name': 'id',
                               'project_id': self.proxy.get_project_id()
                           })

    def test_subnets(self):
        self.verify_list(self.proxy.subnets, subnet.Subnet,
                         expected_kwargs={
                             'project_id': self.proxy.get_project_id()
                         })

    def test_subnet_find(self):
        self.verify_find(self.proxy.find_subnet, subnet.Subnet, 'id',
                         expected_kwargs={
                             'project_id': self.proxy.get_project_id()
                         })

    def test_subnet_get(self):
        self.verify_get(self.proxy.get_subnet, subnet.Subnet, 'id',
                        expected_kwargs={
                            'project_id': self.proxy.get_project_id(),
                        })

    def test_subnet_update(self):
        self.verify_update(self.proxy.update_subnet, subnet.Subnet,
                           method_kwargs={'vpc_id': 'vpc'},
                           expected_kwargs={
                               'base_path': subnet.vpc_subnet_base_path('vpc'),
                               'project_id': self.proxy.get_project_id(),
                           })

    def test_subnet_delete(self):
        self.verify_delete(
            self.proxy.delete_subnet, subnet.Subnet, True,
            mock_method='otcextensions.sdk.vpc.v1._proxy.Proxy._delete',
            method_kwargs={'vpc_id': 'vpc'},
            expected_kwargs={
                'ignore_missing': True,
                'base_path': subnet.vpc_subnet_base_path('vpc'),
            })
