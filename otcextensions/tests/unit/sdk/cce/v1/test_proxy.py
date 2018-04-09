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

from otcextensions.sdk.cce.v1 import _proxy
from otcextensions.sdk.cce.v1 import cluster as _cluster
from otcextensions.sdk.cce.v1 import cluster_host as _cluster_host


class TestCCEProxy(test_proxy_base.TestProxyBase):
    # HEADERS = {
    #     'Content-Type': 'application/json'
    # }

    def setUp(self):
        super(TestCCEProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestCCECluster(TestCCEProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.clusters, _cluster.Cluster,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_kwargs={},
            paginated=False,
            expected_kwargs={}
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_cluster,
            _cluster.Cluster,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._get',
            expected_kwargs={}
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_cluster,
            _cluster.Cluster, True,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._delete',
            expected_kwargs={}
        )


class TestCCEClusterNode(TestCCEProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.cluster_nodes, _cluster_host.ClusterHost,
            mock_method='otcextensions.sdk.sdk_proxy.Proxy._list',
            method_args=['cluster'],
            method_kwargs={},
            paginated=False,
            expected_kwargs={
                'cluster_uuid': 'cluster'
            }
        )

    def test_get(self):
        self._verify2(
            'otcextensions.sdk.sdk_proxy.Proxy._get',
            self.proxy.get_cluster_node,
            method_args=['cluster', 'node'],
            expected_args=[_cluster_host.ClusterHost, 'node'],
            expected_kwargs={
                'cluster_uuid': 'cluster'
            }
        )

    def test_add_node(self):
        attrs = {'a': 'b'}
        self._verify2(
            'otcextensions.sdk.cce.v1.cluster_host.ClusterHost.create',
            self.proxy.add_node,
            method_args=['cluster_uuid'],
            method_kwargs=attrs,
            expected_args=[self.proxy],
            expected_kwargs={
                'endpoint_override': None,
                'headers': None,
                'prepend_key': True
            }
        )

    def test_delete_nodes(self):
        self._verify2(
            'otcextensions.sdk.cce.v1.cluster.Cluster.delete_nodes',
            self.proxy.delete_cluster_nodes,
            method_args=['cluster_uuid', ['n1', 'n2']],
            expected_args=[self.proxy, ['n1', 'n2']],
            expected_kwargs={}
        )
