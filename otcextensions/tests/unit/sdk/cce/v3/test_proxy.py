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
import mock
from openstack.tests.unit import test_proxy_base

from otcextensions.sdk.cce.v3 import _proxy
from otcextensions.sdk.cce.v3 import cluster as _cluster
from otcextensions.sdk.cce.v3 import cluster_node as _cluster_node
from otcextensions.sdk.cce.v3 import node_pool as _node_pool
from otcextensions.sdk.cce.v3 import cluster_cert as _cluster_cert
from otcextensions.sdk.cce.v3 import job as _job


class TestCCEProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestCCEProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)


class TestCCECluster(TestCCEProxy):

    def test_list(self):
        self.verify_list(
            self.proxy.clusters, _cluster.Cluster,
            # method_kwargs={},
            expected_kwargs={
                'paginated': False
            }
        )

    def test_get(self):
        self.verify_get(
            self.proxy.get_cluster,
            _cluster.Cluster,
            expected_kwargs={}
        )

    def test_create(self):
        self.verify_create(
            self.proxy.create_cluster, _cluster.Cluster,
            method_kwargs={
                'instance': 'test',
                'name': 'some_name'
            },
            expected_kwargs={
                'prepend_key': False,
                'instance': 'test',
                'name': 'some_name'
            }
        )

    def test_delete(self):
        self.verify_delete(
            self.proxy.delete_cluster,
            _cluster.Cluster, True,
            expected_kwargs={}
        )

    def test_get_certs(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._get',
            self.proxy.get_cluster_certificates,
            method_args=[cluster],
            expected_args=[_cluster_cert.ClusterCertificate],
            expected_kwargs={
                'cluster_id': cluster.id,
                'requires_id': False
            }
        )


class TestCCEClusterNode(TestCCEProxy):

    def test_list(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self.verify_list(
            self.proxy.cluster_nodes, _cluster_node.ClusterNode,
            method_args=[cluster],
            method_kwargs={},
            expected_kwargs={
                'paginated': False,
                'cluster_id': cluster.id
            }
        )

    def test_get(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._get',
            self.proxy.get_cluster_node,
            method_args=[cluster, 'node'],
            expected_args=[_cluster_node.ClusterNode, 'node'],
            expected_kwargs={
                'cluster_id': cluster.id
            }
        )

    def test_find(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._find',
            self.proxy.find_cluster_node,
            method_args=[cluster, 'node'],
            expected_args=[_cluster_node.ClusterNode, 'node'],
            expected_kwargs={
                'cluster_id': cluster.id
            }
        )

    def test_add_node(self):
        attrs = {'a': 'b'}
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._create',
            self.proxy.create_cluster_node,
            method_args=[cluster],
            method_kwargs=attrs,
            expected_args=[_cluster_node.ClusterNode],
            expected_kwargs=dict(
                cluster_id=cluster.id,
                **attrs
            )
        )

    def test_delete_node(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._delete',
            self.proxy.delete_cluster_node,
            method_args=[cluster, 'n1'],
            expected_args=[_cluster_node.ClusterNode, 'n1'],
            expected_kwargs={
                'cluster_id': cluster.id,
                'ignore_missing': True
            }
        )

    def test_server_wait_for(self):
        value = _cluster.Cluster(id='cluster_id')
        self.verify_wait_for_status(
            self.proxy.wait_for_cluster,
            method_args=[value],
            expected_args=[value, 'Available', ['ERROR'], 2, 960],
            expected_kwargs={'attribute': 'status.status'})


class TestCCENodePool(TestCCEProxy):

    def test_list_node_pool(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self.verify_list(
            self.proxy.node_pools, _node_pool.NodePool,
            method_args=[cluster],
            method_kwargs={},
            expected_kwargs={
                'paginated': False,
                'cluster_id': cluster.id
            }
        )

    def test_get_node_pool(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._get',
            self.proxy.get_node_pool,
            method_args=[cluster, 'node_pool'],
            expected_args=[_node_pool.NodePool, 'node_pool'],
            expected_kwargs={
                'cluster_id': cluster.id
            }
        )

    def test_find_node_pool(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._find',
            self.proxy.find_node_pool,
            method_args=[cluster, 'node_pool'],
            expected_args=[_node_pool.NodePool, 'node_pool'],
            expected_kwargs={
                'cluster_id': cluster.id
            }
        )

    def test_add_node_pool(self):
        attrs = {'a': 'b'}
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._create',
            self.proxy.create_node_pool,
            method_args=[cluster],
            method_kwargs=attrs,
            expected_args=[_node_pool.NodePool],
            expected_kwargs=dict(
                cluster_id=cluster.id,
                **attrs
            )
        )

    def test_delete_node_pool(self):
        cluster = _cluster.Cluster(id='cluster_id')
        self._verify2(
            'openstack.proxy.Proxy._delete',
            self.proxy.delete_node_pool,
            method_args=[cluster, 'n1'],
            expected_args=[_node_pool.NodePool, 'n1'],
            expected_kwargs={
                'cluster_id': cluster.id,
                'ignore_missing': True
            }
        )


class TestCCEJob(TestCCEProxy):
    def test_get(self):
        self.verify_get(
            self.proxy.get_job,
            _job.Job,
            expected_kwargs={}
        )

    def test_wait_for_job(self):
        self.proxy.get_job = mock.Mock(return_value='some_fake')
        self.verify_wait_for_status(
            self.proxy.wait_for_job,
            method_args=['fake_job_id'],
            expected_args=['some_fake', 'success', ['FAILED'], 5, 3600],
            expected_kwargs={'attribute': 'status.status'}
        )
        self.proxy.get_job.assert_called_with('fake_job_id')


class TestExtractName(TestCCEProxy):

    def test_extract_name(self):

        self.assertEqual(
            ['discovery'],
            self.proxy._extract_name('/api/v3/projects/123', project_id='123')
        )
        self.assertEqual(
            ['clusters'],
            self.proxy._extract_name(
                '/api/v3/projects/123/clusters', project_id='123')
        )
        self.assertEqual(
            ['cluster'],
            self.proxy._extract_name(
                '/api/v3/projects/123/clusters/c1', project_id='123')
        )
        self.assertEqual(
            ['cluster', 'clustercert'],
            self.proxy._extract_name(
                '/api/v3/projects/123/clusters/c1/clustercert',
                project_id='123')
        )
        self.assertEqual(
            ['cluster', 'nodes'],
            self.proxy._extract_name(
                '/api/v3/projects/123/clusters/c1/nodes', project_id='123')
        )
        self.assertEqual(
            ['cluster', 'node'],
            self.proxy._extract_name(
                '/api/v3/projects/123/clusters/c1/nodes/n1', project_id='123')
        )
