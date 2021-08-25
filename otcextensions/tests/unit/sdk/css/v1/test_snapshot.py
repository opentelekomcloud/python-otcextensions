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

from openstack.tests.unit import base

from otcextensions.sdk.css.v1 import snapshot


FAKE_ID = "68d5745e-6af2-40e4-945d-fe449be00148"
EXAMPLE = {
    "created": "2018-03-07T07:34:47",
    "datastore": {
        "type": "elasticsearch",
        "version": "6.2.3"
    },
    "description": "",
    "id": FAKE_ID,
    "clusterId": "37cb1075-c38e-4cd8-81df-442d52df3786",
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
    "version": "6.2.3",
    "restoreStatus": "success",
    "startTime": 1520408087099,
    "endTime": 1520408412219,
    "bucketName": "obs-b8ed"
}


class TestSnapshot(base.TestCase):

    def setUp(self):
        super(TestSnapshot, self).setUp()

    def test_basic(self):
        sot = snapshot.Snapshot()

        self.assertEqual(
            '/clusters/%(clusterId)s/index_snapshot', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = snapshot.Snapshot(**EXAMPLE)
        not_sot_attrs = (
            'clusterId',
            'datastore',
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
            EXAMPLE['backupExpectedStartTime'], sot.backup_start_time)
        self.assertEqual(EXAMPLE['backupKeepDay'], sot.backup_keep_days)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['totalShards'], sot.total_shards)
        self.assertEqual(EXAMPLE['failedShards'], sot.failed_shards)
        self.assertEqual(EXAMPLE['startTime'], sot.start_time)
        self.assertEqual(EXAMPLE['endTime'], sot.end_time)
        self.assertEqual(EXAMPLE['bucketName'], sot.bucket_name)
        self.assertEqual(EXAMPLE['datastore']['type'], sot.datastore.type)
        self.assertEqual(EXAMPLE['datastore']['version'],
                         sot.datastore.version)
        self.assertEqual(EXAMPLE['restoreStatus'], sot.restore_status)
        for key, value in EXAMPLE.items():
            if key in not_sot_attrs:
                pass
            else:
                self.assertEqual(getattr(sot, key), value)
