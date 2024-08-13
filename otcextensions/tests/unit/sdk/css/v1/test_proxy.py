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
from otcextensions.sdk.css.v1 import _proxy
from otcextensions.sdk.css.v1 import cert as _cert
from otcextensions.sdk.css.v1 import cluster as _cluster
from otcextensions.sdk.css.v1 import cluster_image as _cluster_image
from otcextensions.sdk.css.v1 import cluster_upgrade_info \
    as _cluster_upgrade_info
from otcextensions.sdk.css.v1 import flavor as _flavor
from otcextensions.sdk.css.v1 import snapshot as _snapshot

ENDPOINT_CSS = 'http://css.example.com/v1.0'


class TestCssProxy(test_proxy_base.TestProxyBase):
    def setUp(self):
        super(TestCssProxy, self).setUp()
        self.proxy = _proxy.Proxy(self.session)
        self.session.get_endpoint = mock.Mock(return_value=ENDPOINT_CSS)

    def test_clusters(self):
        self.verify_list(
            self.proxy.clusters,
            _cluster.Cluster,
            method_kwargs={'id': 'foo', 'start': 999, 'limit': 666},
            expected_kwargs={'id': 'foo', 'start': 999, 'limit': 666},
        )

    def test_get_cluster(self):
        self.verify_get(self.proxy.get_cluster, _cluster.Cluster)

    def test_find_cluster(self):
        self.verify_find(self.proxy.find_cluster, _cluster.Cluster, False)

    def test_create_cluster(self):
        self.verify_create(
            self.proxy.create_cluster,
            _cluster.Cluster,
            method_kwargs={'x': 1, 'y': 2, 'z': 3},
            expected_kwargs={'x': 1, 'y': 2, 'z': 3},
        )

    def test_delete_cluster(self):
        self.verify_delete(self.proxy.delete_cluster, _cluster.Cluster, True)

    def test_restart_cluster(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.restart',
            self.proxy.restart_cluster,
            method_args=[_cluster.Cluster],
            expected_args=[self.proxy],
        )

    def test_extend_cluster(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.extend',
            self.proxy.extend_cluster,
            method_args=[_cluster.Cluster, 2],
            expected_args=[self.proxy, 2],
        )

    def test_extend_cluster_nodes(self):
        self.verify_create(
            self.proxy.extend_cluster_nodes,
            _cluster.ExtendClusterNodes,
            method_kwargs={
                'cluster': 'cluster-uuid',
                'grow': [{'x': 1, 'y': 2, 'z': 3}],
            },
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'grow': [{'x': 1, 'y': 2, 'z': 3}],
            },
        )

    def test_update_cluster_name(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_name',
            self.proxy.update_cluster_name,
            method_args=[_cluster.Cluster, 'test'],
            expected_args=[self.proxy, 'test'],
        )

    def test_update_password(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_password',
            self.proxy.update_cluster_password,
            method_args=[_cluster.Cluster, 'password'],
            expected_args=[self.proxy, 'password'],
        )

    def test_update_security_mode(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_security_mode',
            self.proxy.update_cluster_security_mode,
            method_args=[_cluster.Cluster, False, None, True],
            expected_args=[self.proxy, False, None, True],
        )

        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_security_mode',
            self.proxy.update_cluster_security_mode,
            method_kwargs={
                'cluster': _cluster.Cluster,
                'authority_enable': False,
                'admin_pwd': None,
                'https_enable': False,
            },
            expected_args=[self.proxy, False, None, False],
        )

    def test_update_security_group(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_security_group',
            self.proxy.update_cluster_security_group,
            method_args=[_cluster.Cluster, 'security-group.id'],
            expected_args=[self.proxy, 'security-group.id'],
        )

    def test_update_cluster_flavor(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_flavor',
            self.proxy.update_cluster_flavor,
            method_kwargs={
                'cluster': _cluster.Cluster,
                'new_flavor': 'test',
                'check_replica': True,
            },
            expected_args=[self.proxy, 'test', None, True],
        )

        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_flavor',
            self.proxy.update_cluster_flavor,
            method_args=[_cluster.Cluster, 'test', 'ess', True],
            expected_args=[self.proxy, 'test', 'ess', True],
        )

    def test_update_kernel(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.update_kernel',
            self.proxy.update_cluster_kernel,
            method_args=[
                _cluster.Cluster,
                'target-image-id',
                'upgrade-type',
                True,
                'agency',
                False,
            ],
            expected_args=[
                self.proxy,
                'target-image-id',
                'upgrade-type',
                True,
                'agency',
                False,
            ],
        )

    def test_get_cluster_upgrade_version_info(self):
        self.verify_get(
            self.proxy.get_cluster_version_upgrade_info,
            _cluster_image.ClusterImage,
            method_args=[],
            method_kwargs={'cluster': 'test_id', 'upgrade_type': 'cross'},
            expected_kwargs={
                'cluster_id': 'test_id',
                'upgrade_type': 'cross',
                'requires_id': False,
            },
        )

    def test_scale_in_cluster(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.scale_in',
            self.proxy.scale_in_cluster,
            method_args=[_cluster.Cluster, ['node-id']],
            expected_args=[self.proxy, ['node-id']],
        )

    def test_scale_in_cluster_by_node_type(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.scale_in_by_node_type',
            self.proxy.scale_in_cluster_by_node_type,
            method_args=[
                _cluster.Cluster,
                [{'type': 'node-type', 'reducedNodeNum': 1}],
            ],
            expected_args=[
                self.proxy,
                [{'type': 'node-type', 'reducedNodeNum': 1}],
            ],
        )

    def test_replace_cluster_node(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.replace_node',
            self.proxy.replace_cluster_node,
            method_args=[_cluster.Cluster, 'node-id'],
            expected_args=[self.proxy, 'node-id'],
        )

    def test_add_cluster_nodes(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.add_nodes',
            self.proxy.add_cluster_nodes,
            method_args=[
                _cluster.Cluster,
                'node-type',
                'flavor',
                3,
                'volume-type',
            ],
            expected_args=[
                self.proxy,
                'node-type',
                'flavor',
                3,
                'volume-type',
            ],
        )

    def test_get_cluster_upgrade_info(self):
        self.verify_list(
            self.proxy.get_cluster_upgrade_info,
            _cluster_upgrade_info.ClusterUpgradeInfo,
            method_kwargs={'cluster': 'cluster-uuid'},
            expected_kwargs={'cluster_id': 'cluster-uuid'},
        )

    def test_retry_cluster_upgrade_job(self):
        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.retry_upgrade_job',
            self.proxy.retry_cluster_upgrade_job,
            method_kwargs={
                'cluster': _cluster.Cluster,
                'job_id': 'job-id',
                'retry_mode': None,
            },
            expected_args=[self.proxy, 'job-id', None],
        )

        self._verify(
            'otcextensions.sdk.css.v1.cluster.Cluster.retry_upgrade_job',
            self.proxy.retry_cluster_upgrade_job,
            method_args=[_cluster.Cluster, 'job-id', 'abort'],
            expected_args=[self.proxy, 'job-id', 'abort'],
        )

    def test_flavors(self):
        self.verify_list(
            self.proxy.flavors,
            _flavor.Flavor,
        )

    def test_snapshots(self):
        self._verify(
            'openstack.proxy.Proxy._list',
            self.proxy.snapshots,
            method_args=['cluster-uuid'],
            expected_args=[_snapshot.Snapshot],
            expected_kwargs={
                'base_path': '/clusters/cluster-uuid/index_snapshots'
            },
        )

    def test_create_snapshot(self):
        self.verify_create(
            self.proxy.create_snapshot,
            _snapshot.Snapshot,
            method_kwargs={'cluster': 'cluster-uuid', 'x': 1, 'y': 2},
            expected_kwargs={
                'uri_cluster_id': 'cluster-uuid',
                'x': 1,
                'y': 2,
            },
        )

    def test_find_snapshot(self):
        self._verify(
            'openstack.proxy.Proxy._find',
            self.proxy.find_snapshot,
            method_args=['cluster-uuid', 'snapshot-uuid'],
            expected_args=[_snapshot.Snapshot, 'snapshot-uuid'],
            expected_kwargs={
                'base_path': '/clusters/cluster-uuid/index_snapshots',
                'ignore_missing': True,
            },
        )

    def test_delete_snapshot(self):
        self._verify(
            'openstack.proxy.Proxy._delete',
            self.proxy.delete_snapshot,
            method_args=['cluster-uuid', 'snapshot-uuid', False],
            expected_args=[_snapshot.Snapshot, 'snapshot-uuid'],
            expected_kwargs={
                'uri_cluster_id': 'cluster-uuid',
                'ignore_missing': False,
            },
        )

    def test_restore_snapshot(self):
        self._verify(
            'otcextensions.sdk.css.v1.snapshot.Snapshot.restore',
            self.proxy.restore_snapshot,
            method_args=[_cluster.Cluster, _snapshot.Snapshot],
            method_kwargs={'a': '1', 'b': '2'},
            expected_args=[self.proxy, _cluster.Cluster],
            expected_kwargs={'a': '1', 'b': '2'},
        )

    def test_set_snapshot_configuration(self):
        self.verify_create(
            self.proxy.set_snapshot_configuration,
            _snapshot.SnapshotConfiguration,
            method_kwargs={
                'cluster': 'cluster-uuid',
                'auto_configure': False,
                'x': 1,
                'y': 2,
            },
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'setting': 'setting',
                'x': 1,
                'y': 2,
            },
        )

    def test_disable_snapshot_function(self):
        self._verify(
            'otcextensions.sdk.css.v1.snapshot.SnapshotConfiguration.disable',
            self.proxy.disable_snapshot_function,
            method_args=['cluster-uuid'],
            expected_args=[self.proxy],
        )

    def test_set_snapshot_policy(self):
        self.verify_create(
            self.proxy.set_snapshot_policy,
            _snapshot.SnapshotPolicy,
            method_kwargs={'cluster': 'cluster-uuid', 'x': 1, 'y': 2},
            expected_kwargs={'cluster_id': 'cluster-uuid', 'x': 1, 'y': 2},
        )

    def test_get_snapshot_policy(self):
        self._verify(
            'openstack.proxy.Proxy._get',
            self.proxy.get_snapshot_policy,
            method_args=['cluster-uuid'],
            expected_args=[_snapshot.SnapshotPolicy],
            expected_kwargs={
                'cluster_id': 'cluster-uuid',
                'requires_id': False,
            },
        )

    def test_get_certificate(self):
        self._verify(
            'openstack.proxy.Proxy._get',
            self.proxy.get_certificate,
            expected_args=[_cert.Cert],
            expected_kwargs={'requires_id': False},
        )
