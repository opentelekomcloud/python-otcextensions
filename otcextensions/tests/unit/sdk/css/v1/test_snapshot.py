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
import uuid

import mock
from keystoneauth1 import adapter

from openstack import utils
from openstack.tests.unit import base
from otcextensions.sdk.css.v1 import snapshot

EXAMPLE = {
    "created": "2018-03-07T07:34:47",
    "datastore": {"type": "elasticsearch", "version": "7.6.2"},
    "description": "",
    "id": uuid.uuid4().hex,
    "clusterId": uuid.uuid4().hex,
    "clusterName": "Es-xfx",
    "name": "snapshot-002",
    "status": "COMPLETED",
    "updated": "2018-03-07T07:40:12",
    "backupType": "1",
    "backupMethod": "manual",
    "backupExpectedStartTime": None,
    "backupKeepDay": None,
    "backupPeriod": None,
    "indices": ".kibana,website2",
    "totalShards": 6,
    "failedShards": 0,
    "version": "7.6.2",
    "restoreStatus": "success",
    "startTime": 1520408087099,
    "endTime": 1520408412219,
    "bucketName": "obs-b8ed",
}

EXAMPLE_POLICY = {
    "keepday": 2,
    "period": "16:00 GMT+08:00",
    "prefix": "snapshot",
    "bucket": "es-backup",
    "basePath": "css_repository/tests",
    "agency": "usearch",
    "enable": "true",
    "indeices": "*",
    "snapshotCmkId": uuid.uuid4().hex,
}


class TestSnapshot(base.TestCase):

    def setUp(self):
        super(TestSnapshot, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = snapshot.Snapshot()

        self.assertEqual(
            '/clusters/%(uri_cluster_id)s/index_snapshot', sot.base_path
        )
        self.assertEqual('backup', sot.resource_key)
        self.assertEqual('backups', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = snapshot.Snapshot(**EXAMPLE)
        updated_sot_attrs = (
            'clusterId',
            'clusterName',
            'backupType',
            'backupMethod',
            'backupPeriod',
            'backupExpectedStartTime',
            'backupKeepDay',
            'totalShards',
            'failedShards',
            'startTime',
            'endTime',
            'bucketName',
            'restoreStatus',
            'created',
            'updated',
        )
        self.assertEqual(EXAMPLE['clusterId'], sot.cluster_id)
        self.assertEqual(EXAMPLE['clusterName'], sot.cluster_name)
        self.assertEqual(EXAMPLE['backupType'], sot.backup_type)
        self.assertEqual(EXAMPLE['backupMethod'], sot.backup_method)
        self.assertEqual(EXAMPLE['backupPeriod'], sot.backup_period)
        self.assertEqual(
            EXAMPLE['backupExpectedStartTime'], sot.backup_start_time
        )
        self.assertEqual(EXAMPLE['backupKeepDay'], sot.backup_keep_days)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['totalShards'], sot.total_shards)
        self.assertEqual(EXAMPLE['failedShards'], sot.failed_shards)
        self.assertEqual(EXAMPLE['startTime'], sot.start_time)
        self.assertEqual(EXAMPLE['endTime'], sot.end_time)
        self.assertEqual(EXAMPLE['bucketName'], sot.bucket_name)
        self.assertEqual(EXAMPLE['restoreStatus'], sot.restore_status)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_restore(self):
        sot = snapshot.Snapshot.existing(id=EXAMPLE['id'])
        cluster_id = uuid.uuid4().hex
        json_body = {
            "targetCluster": uuid.uuid4().hex,
            "indices": "myindex1,myindex2",
        }
        response = mock.Mock()
        response.status_code = 201
        response.headers = {}
        self.sess.post.return_value = response

        rt = sot.restore(self.sess, cluster_id, **json_body)
        uri = utils.urljoin(
            'clusters', cluster_id, 'index_snapshot', sot.id, 'restore'
        )
        self.sess.post.assert_called_with(uri, json=json_body)

        self.assertIsNone(rt)


class TestSnapshotPolicy(base.TestCase):

    def setUp(self):
        super(TestSnapshotPolicy, self).setUp()

    def test_basic(self):
        sot = snapshot.SnapshotPolicy()

        self.assertEqual(
            '/clusters/%(cluster_id)s/index_snapshot/policy', sot.base_path
        )
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = snapshot.SnapshotPolicy(**EXAMPLE_POLICY)
        self.assertEqual(EXAMPLE_POLICY['agency'], sot.agency)
        self.assertEqual(EXAMPLE_POLICY['basePath'], sot.backup_path)
        self.assertEqual(EXAMPLE_POLICY['period'], sot.backup_period)
        self.assertEqual(EXAMPLE_POLICY['keepday'], sot.backup_keep_days)
        self.assertEqual(EXAMPLE_POLICY['bucket'], sot.bucket_name)
        self.assertEqual(EXAMPLE_POLICY['snapshotCmkId'], sot.cmk_id)
        self.assertEqual(EXAMPLE_POLICY['prefix'], sot.prefix)
        self.assertEqual(bool(EXAMPLE_POLICY['enable']), sot.is_enabled)


class TestSnapshotConfiguration(base.TestCase):

    def setUp(self):
        super(TestSnapshotConfiguration, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = snapshot.SnapshotConfiguration()

        self.assertEqual(
            '/clusters/%(cluster_id)s/index_snapshot/%(setting)s',
            sot.base_path,
        )
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_disable(self):
        sot = snapshot.SnapshotConfiguration.existing(
            cluster_id=EXAMPLE['id']
        )
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        self.sess.delete.return_value = response

        rt = sot.disable(self.sess)
        uri = utils.urljoin('clusters', sot.cluster_id, 'index_snapshots')
        self.sess.delete.assert_called_with(uri)

        self.assertIsNone(rt)
