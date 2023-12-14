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

from otcextensions.sdk.dws.v1 import _proxy
from otcextensions.sdk.dws.v1 import cluster as _cluster
from otcextensions.sdk.dws.v1 import snapshot as _snapshot
from otcextensions.sdk.dws.v1 import flavor as _flavor
from otcextensions.sdk.dws.v1 import tag as _tag

from openstack.tests.unit import test_proxy_base


ENDPOINT_DWS = 'http://dws.example.com/v1.0'


class TestDwsProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestDwsProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_endpoint = mock.Mock(
            return_value=ENDPOINT_DWS
        )

    def test_clusters(self):
        self.verify_list(
            self.proxy.clusters,
            _cluster.Cluster,
        )

    def test_get_cluster(self):
        self.verify_get(self.proxy.get_cluster, _cluster.Cluster)

    def test_find_cluster(self):
        self.verify_find(self.proxy.find_cluster, _cluster.Cluster, False)

    def test_create_cluster(self):
        self.verify_create(
            self.proxy.create_cluster, _cluster.Cluster,
            method_kwargs={'x': 1, 'y': 2, 'z': 3},
            expected_kwargs={
                'x': 1, 'y': 2, 'z': 3
            }
        )

    def test_delete_cluster(self):
        self._verify(
            "openstack.proxy.Proxy._delete",
            self.proxy.delete_cluster,
            method_args=['cluster-uuid', 0, True],
            expected_args=[_cluster.Cluster, 'cluster-uuid'],
            expected_kwargs={
                'keep_last_manual_snapshot': 0,
                'ignore_missing': True
            }
        )

    def test_restart_cluster(self):
        self._verify(
            'otcextensions.sdk.dws.v1.cluster.Cluster.restart',
            self.proxy.restart_cluster,
            method_args=[_cluster.Cluster],
            expected_args=[self.proxy]
        )

    def test_scale_out_cluster(self):
        self._verify(
            'otcextensions.sdk.dws.v1.cluster.Cluster.scale_out',
            self.proxy.scale_out_cluster,
            method_args=[_cluster.Cluster, 2],
            expected_args=[self.proxy, 2]
        )

    def test_reset_password(self):
        self._verify(
            'otcextensions.sdk.dws.v1.cluster.Cluster.reset_password',
            self.proxy.reset_password,
            method_args=[_cluster.Cluster, 'TestNewPassword'],
            expected_args=[self.proxy, 'TestNewPassword']
        )

    def test_snapshots(self):
        self.verify_list(
            self.proxy.snapshots,
            _snapshot.Snapshot,
        )

    def test_get_snapshot(self):
        self.verify_get(self.proxy.get_snapshot, _snapshot.Snapshot)

    def test_find_snapshot(self):
        self.verify_find(self.proxy.find_snapshot, _snapshot.Snapshot, False)

    def test_create_snapshot(self):
        self.verify_create(
            self.proxy.create_snapshot,
            _snapshot.Snapshot,
            method_kwargs={
                'x': 1, 'y': 2
            },
            expected_kwargs={
                'x': 1, 'y': 2
            }
        )

    def test_restore_snapshot(self):
        self.verify_create(
            self.proxy.restore_snapshot, _snapshot.Restore,
            method_args=['snapshot-uuid'],
            method_kwargs={
                'x': 1, 'y': 2, 'z': 3
            },
            expected_args=[],
            expected_kwargs={
                'snapshot_id': 'snapshot-uuid',
                'x': 1, 'y': 2, 'z': 3,
            },
        )

    def test_delete_snapshot(self):
        self._verify(
            "openstack.proxy.Proxy._delete",
            self.proxy.delete_snapshot,
            method_args=['snapshot-uuid', True],
            expected_args=[_snapshot.Snapshot, 'snapshot-uuid'],
            expected_kwargs={
                'ignore_missing': True
            }
        )

    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors,
            _flavor.Flavor,
        )

    def test_list_cluster_tags(self):
        self.verify_list(
            self.proxy.list_cluster_tags,
            _tag.Tag,
            method_args=["test_cluster_id"],
            expected_kwargs={'cluster_id': 'test_cluster_id'},
            expected_args=[]
        )

    def test_create_cluster_tag(self):
        tag = {'key': 'key1', 'value': 'value1'}
        self.verify_create(
            self.proxy.create_cluster_tag,
            _tag.Tag,
            method_args=['test_cluster_id', tag],
            method_kwargs={},
            expected_kwargs={
                'cluster_id': 'test_cluster_id',
                'key': 'key1', 'value': 'value1'
            },
            expected_args=[]
        )

    def test_delete_cluster_tag(self):
        self.verify_delete(
            self.proxy.delete_cluster_tag,
            _tag.Tag,
            method_args=['test_cluster_id', 'key1'],
            method_kwargs={},
            expected_kwargs={
                'cluster_id': 'test_cluster_id',
                'ignore_missing': True
            },
            expected_args=['key1']
        )

    # Tests for batch operations
    def test_batch_create_cluster_tags(self):
        self._verify(
            'otcextensions.sdk.dws.v1.tag.Tag.manage_tags_batch',
            self.proxy.batch_create_cluster_tags,
            method_args=[
                'test_cluster_id',
                [
                    {'key': 'key1', 'value': 'value1'},
                    {'key': 'key2', 'value': 'value2'}
                ]
            ],
            expected_args=[
                self.proxy,
                'test_cluster_id',
                [
                    {'key': 'key1', 'value': 'value1'},
                    {'key': 'key2', 'value': 'value2'}
                ],
                'create'
            ],
            expected_kwargs={}
        )

    def test_batch_delete_cluster_tags(self):
        self._verify(
            'otcextensions.sdk.dws.v1.tag.Tag.manage_tags_batch',
            self.proxy.batch_delete_cluster_tags,
            method_args=[
                'test_cluster_id',
                [
                    {'key': 'key1'},
                    {'key': 'key2'}
                ]
            ],
            expected_args=[
                self.proxy,
                'test_cluster_id',
                [{'key': 'key1'}, {'key': 'key2'}],
                'delete'
            ],
            expected_kwargs={}
        )
