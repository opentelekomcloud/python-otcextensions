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
            '/clusters/%(cluster_id)s/index_snapshot', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_get)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = snapshot.Snapshot(**EXAMPLE)
        for key, value in EXAMPLE.items():
            if key == 'datastore':
                self.assertEqual(
                    getattr(sot.datastore, 'type'), 'elasticsearch')
                self.assertEqual(getattr(sot.datastore, 'version'), '6.2.3')
            else:
                self.assertEqual(getattr(sot, key), value)
