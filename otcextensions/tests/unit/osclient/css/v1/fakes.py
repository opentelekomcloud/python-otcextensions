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
#
import uuid
from collections import defaultdict
# from datetime import datetime

import mock

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.css.v1 import cluster
from otcextensions.sdk.css.v1 import snapshot


def gen_data(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(getattr(data, attr, '') for attr in columns)


def gen_data_dict(data, columns):
    """Fill expected data tuple based on columns list
    """
    return tuple(data.get(attr, '') for attr in columns)


class TestCss(utils.TestCommand):
    def setUp(self):
        super(TestCss, self).setUp()

        self.app.client_manager.css = mock.Mock()

        self.client = self.app.client_manager.css


class FakeCluster(test_base.Fake):
    """Fake one or more Nat Gateways."""
    @classmethod
    def generate(cls):
        """Create a fake CSS Cluster.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "datastore": {
                "type": "elasticsearch",
                "version": "7.6.2"
            },
            "instances": [
                {
                    "status": "200",
                    "type": "ess",
                    "id": "id-" + uuid.uuid4().hex,
                    "name": "css-" + uuid.uuid4().hex,
                    "specCode": "css.xlarge.2",
                    "azCode": "eu-de-01"
                }
            ],
            "updated": "2020-12-03T07:02:08",
            "name": "name-" + uuid.uuid4().hex,
            "created": "2020-12-03T07:02:08",
            "id": "id-" + uuid.uuid4().hex,
            "status": "200",
            "endpoint": "x.x.x.x:9200",
            "vpcId": "router-" + uuid.uuid4().hex,
            "subnetId": "subnet-" + uuid.uuid4().hex,
            "securityGroupId": "security-group-" + uuid.uuid4().hex,
            "httpsEnable": True,
            "authorityEnable": True,
            "diskEncrypted": False,
            "actionProgress": {},
            "actions": [],
            "tags": []
        }
        obj = cluster.Cluster(**object_info)
        setattr(obj, 'version', obj.datastore.version)
        setattr(obj, 'type', obj.datastore.type)
        node_count = defaultdict(int)
        for node in obj.nodes:
            node_count[node['type']] += 1
        setattr(obj, 'node_count', dict(node_count))
        return obj


class FakeSnapshot(test_base.Fake):
    """Fakse one or more Snapshot"""
    @classmethod
    def generate(cls):
        """Create a fake CSS Snapshot.

        :return:
            A FakeResource object, with id, name and so on
        """
        object_info = {
            "created": "2018-03-07T07:34:47",
            "datastore": {
                "type": "elasticsearch",
                "version": "6.2.3"
            },
            "description": "",
            "id": "id-" + uuid.uuid4().hex,
            "clusterId": "cluster_id-" + uuid.uuid4().hex,
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
        return snapshot.Snapshot(**object_info)


class FakeSnapshotPolicy(test_base.Fake):
    """Fake one or more Snapshot Policy."""
    @classmethod
    def generate(cls):
        """Create a fake CSS Snapshot Policy.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "keepday": 2,
            "period": "16:00 GMT+08:00",
            "prefix": "snapshot",
            "bucket": "test-bucket",
            "basePath": "css_repository/tests",
            "agency": "usearch",
            "enable": "true",
            "snapshotCmkId": "kms-" + uuid.uuid4().hex
        }
        return snapshot.SnapshotPolicy(**object_info)
