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

from otcextensions.sdk.css.v1 import _proxy
from otcextensions.sdk.css.v1 import flavor as _flavor
from otcextensions.sdk.css.v1 import cluster as _cluster
from otcextensions.sdk.css.v1 import snapshot as _snapshot
from otcextensions.sdk.css.v1 import cert as _cert

from openstack.tests.unit import test_proxy_base


ENDPOINT_CSS = 'http://css.example.com/v1.0'


class TestCssProxy(test_proxy_base.TestProxyBase):

    def setUp(self):
        super(TestCssProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_endpoint = mock.Mock(
            return_value=ENDPOINT_CSS
        )

    def test_clusters(self):
        self.verify_list(self.proxy.clusters, _cluster.Cluster)

    def test_get_cluster(self):
        self.verify_get(self.proxy.get_cluster, _cluster.Cluster)

    def test_find_cluster(self):
        self.verify_find(self.proxy.find_cluster, _cluster.Cluster, False)

    def test_create_cluster(self):
        self.verify_create(
            self.proxy.create_cluster, _cluster.Cluster,
            method_kwargs={'x': 1, 'y': 2, 'z': 3},
            expected_kwargs={
                'prepend_key': False,
                'x': 1, 'y': 2, 'z': 3
            }
        )

    def test_delete_cluster(self):
        self.verify_delete(
            self.proxy.delete_cluster, _cluster.Cluster, True
        )

    def test_restart_cluster(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.restart',
            self.proxy.restart_cluster,
            method_args=[_cluster.Cluster],
            expected_args=[self.proxy]
        )

    def test_extend_cluster(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.extend',
            self.proxy.extend_cluster,
            method_args=[_cluster.Cluster, 2],
            expected_args=[self.proxy, 2]
        )

    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors,
            _flavor.Flavor,
        )

    def test_snapshots(self):
        self._verify(
            "openstack.proxy.Proxy._list",
            self.proxy.snapshots,
            method_args=['cluster-uuid'],
            expected_args=[_snapshot.Snapshot],
            expected_kwargs={
                'base_path': '/clusters/cluster-uuid/index_snapshots'
            }
        )

    def test_create_snapshot(self):
        self.verify_create(
            self.proxy.create_snapshot, _snapshot.Snapshot,
            method_kwargs={
                'cluster': 'cluster-uuid',
                'x': 1, 'y': 2
            },
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'prepend_key': False,
                'x': 1, 'y': 2
            }
        )

    def test_delete_snapshot(self):
        self._verify(
            "openstack.proxy.Proxy._delete",
            self.proxy.delete_snapshot,
            method_args=['cluster-uuid', 'snapshot-uuid', True],
            expected_args=[_snapshot.Snapshot, 'snapshot-uuid'],
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'ignore_missing': True
            }
        )

    def test_set_snapshot_configuration(self):
        self.verify_create(
            self.proxy.set_snapshot_configuration,
            _snapshot.SnapshotConfiguration,
            method_kwargs={
                'cluster': 'cluster-uuid',
                'auto_setting': False,
                'x': 1, 'y': 2
            },
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'setting': 'setting',
                'x': 1, 'y': 2
            }
        )

    def test_set_snapshot_policy(self):
        self.verify_create(
            self.proxy.set_snapshot_policy, _snapshot.SnapshotPolicy,
            method_kwargs={
                'cluster': 'cluster-uuid',
                'x': 1, 'y': 2
            },
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'x': 1, 'y': 2
            }
        )

    def test_get_snapshot_policy(self):
        self._verify(
            "openstack.proxy.Proxy._get",
            self.proxy.get_snapshot_policy,
            method_args=['cluster-uuid'],
            expected_args=[_snapshot.SnapshotPolicy],
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'requires_id': False
            }
        )

    def test_restore_snapshot(self):
        self._verify(
            'otcextensions.sdk.css.v1.snapshot.Snapshot.restore',
            self.proxy.restore_snapshot,
            method_args=[_snapshot.Snapshot, 'snapshot-uuid'],
            method_kwargs={'a': '1', 'b': '2'},
            expected_args=[self.proxy],
            expected_kwargs={'a': '1', 'b': '2'},
        )

    def test_disabled_snapshot_function(self):
        self._verify(
            "openstack.proxy.Proxy._delete",
            self.proxy.disable_snapshot_function,
            method_args=['cluster-uuid'],
            expected_args=[_snapshot.Snapshot],
            expected_kwargs={
                'requires_id': False,
                'base_path': '/clusters/cluster-uuid/index_snapshots'
            }
        )

    def test_get_certificate(self):
        self._verify(
            "openstack.proxy.Proxy._get",
            self.proxy.get_certificate,
            expected_args=[_cert.Cert],
            expected_kwargs={'requires_id': False},
        )
