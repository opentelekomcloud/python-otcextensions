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
# from datetime import datetime

import mock

from osc_lib import utils as _osc_lib_utils

from openstackclient.tests.unit import utils
from otcextensions.tests.unit.osclient import test_base

from otcextensions.sdk.css.v1 import cluster
from otcextensions.sdk.css.v1 import flavor
from otcextensions.sdk.css.v1 import snapshot


def gen_data(obj, columns, formatters=None):
    """Fill expected data tuple based on columns list
    """
    return _osc_lib_utils.get_item_properties(
        obj, columns, formatters=formatters
    )


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
            "actionProgress": {},
            "actions": [],
            "authorityEnable": True,
            "backupAvailable": True,
            "bandwidthSize": 5,
            "cmk_id": "cmk-uuid",
            "created": "2023-02-08T23:31:19",
            "datastore": {
                "type": "elasticsearch",
                "version": "7.10.2"
            },
            "diskEncrypted": False,
            "elbWhiteList": {
                "enableWhiteList": False,
                "whiteList": ""
            },
            "endpoint": "192.168.1.67:9200",
            "httpsEnable": True,
            "id": uuid.uuid4().hex,
            "instances": [
                {
                    "azCode": "eu-de-02",
                    "id": uuid.uuid4().hex,
                    "ip": "192.168.1.67",
                    "name": "test-css-d958c4bb-ess-esn-1-1",
                    "specCode": "css.xlarge.4",
                    "status": "200",
                    "type": "ess",
                    "volume": {
                        "size": 100,
                        "type": "HIGH"
                    }
                }
            ],
            "name": "test-css-d958c4bb",
            "period": False,
            "publicIp": "1.2.3.4:9200",
            "publicKibanaResp": None,
            "securityGroupId": uuid.uuid4().hex,
            "status": "200",
            "subnetId": uuid.uuid4().hex,
            "tags": [
                {
                    "key": "123",
                    "value": "11"
                }
            ],
            "updated": "2023-02-08T23:31:19",
            "vpcId": uuid.uuid4().hex
        }
        obj = cluster.Cluster(**object_info)
        setattr(obj, 'num_nodes', len(obj.nodes))
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


class FakeFlavor(test_base.Fake):
    """Fake one or more Flavors."""
    @classmethod
    def generate(cls):
        """Create a fake CSS Snapshot Policy.

        :return:
            A FakeResource object, with id, name and so on
        """
        # Set default attributes.
        object_info = {
            "type": "ess",
            "version": "7.6.2",
            "cpu": 1,
            "ram": 8,
            "name": "css.medium.8",
            "region": "eu-de",
            "diskrange": "40,640",
            "availableAZ": "eu-de-01,eu-de-02,eu-de-03",
            "flavor_id": uuid.uuid4().hex
        }
        return flavor.Flavor(**object_info)
