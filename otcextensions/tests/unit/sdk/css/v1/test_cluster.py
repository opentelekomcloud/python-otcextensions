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
from keystoneauth1 import adapter

import uuid
import mock

from openstack.tests.unit import base

from otcextensions.sdk.css.v1 import cluster


EXAMPLE = {
    "actionProgress": {},
    "actions": [],
    "authorityEnable": True,
    "backupAvailable": True,
    "backupStrategy": {
        "period": "00:00 GMT+03:00",
        "prefix": "backup",
        "keepday": 1,
        "bucket": "css-test-0",
        "agency": "test-css",
        "basePath": "css"
    },
    "bandwidthSize": 5,
    "cmk_id": uuid.uuid4().hex,
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


class TestCluster(base.TestCase):

    def setUp(self):
        super(TestCluster, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = cluster.Cluster()

        self.assertEqual('/clusters', sot.base_path)
        self.assertEqual('cluster', sot.resource_key)
        self.assertEqual('clusters', sot.resources_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_patch)
        self.assertDictEqual({'id': 'id',
                              'start': 'start',
                              'limit': 'limit',
                              'marker': 'marker'},
                             sot._query_mapping._mapping)

    def test_make_it(self):
        sot = cluster.Cluster(**EXAMPLE)
        updated_sot_attrs = (
            'actionProgress',
            'authorityEnable',
            'backupAvailable',
            'backupStrategy',
            'bandwidthSize',
            'created',
            'diskEncrypted',
            'httpsEnable',
            'instances',
            'period',
            'publicIp',
            'publicKibanaResp',
            'securityGroupId',
            'status',
            'subnetId',
            'updated',
            'vpcId',
            'elbWhiteList',
        )

        self.assertEqual(EXAMPLE['actionProgress'], sot.action_progress)
        self.assertEqual(EXAMPLE['authorityEnable'], sot.is_authority_enabled)
        self.assertEqual(EXAMPLE['backupAvailable'], sot.is_backup_enabled)
        self.assertEqual(EXAMPLE['backupStrategy'], sot.backup_strategy)
        self.assertEqual(EXAMPLE['bandwidthSize'], sot.bandwidth_size)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['diskEncrypted'], sot.is_disk_encrypted)
        self.assertEqual(EXAMPLE['httpsEnable'], sot.is_https_enabled)
        self.assertEqual(EXAMPLE['period'], sot.is_billed)
        self.assertEqual(EXAMPLE['publicIp'], sot.floating_ip)
        self.assertEqual(EXAMPLE['publicKibanaResp'], sot.public_kibana_resp)
        self.assertEqual(EXAMPLE['securityGroupId'], sot.security_group_id)
        self.assertEqual(int(EXAMPLE['status']), sot.status_code)
        self.assertEqual(EXAMPLE['subnetId'], sot.network_id)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['vpcId'], sot.router_id)
        self.assertEqual(EXAMPLE['elbWhiteList'], sot.elb_whitelist)

        for i in range(len(sot.nodes)):
            instance = EXAMPLE['instances'][i]
            sot_instance = sot.nodes[i]
            self.assertEqual(
                instance['azCode'], sot_instance.availability_zone
            )
            self.assertEqual(instance['id'], sot_instance.id)
            self.assertEqual(instance['ip'], sot_instance.private_ip)
            self.assertEqual(instance['name'], sot_instance.name)
            self.assertEqual(instance['specCode'], sot_instance.flavor)
            self.assertEqual(instance['status'], sot_instance.status)
            self.assertEqual(instance['type'], sot_instance.node_type)
            self.assertEqual(instance['volume'], sot_instance.volume)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_action(self):
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
        action = "restart"
        json_body = {"restart": {}}
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        self.sess.post.return_value = response

        rt = sot._action(self.sess, action, json_body)
        self.sess.post.assert_called_with(
            'clusters/%s/restart' % sot.id,
            json=json_body)

        self.assertIsNone(rt)

    def test_restart(self):
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
        sot._action = mock.Mock()

        rt = sot.restart(self.sess)
        sot._action.assert_called_with(self.sess, 'restart')
        self.assertIsNone(rt)

    def test_extend(self):
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
        sot._action = mock.Mock()
        node_count = 3

        rt = sot.extend(self.sess, node_count)
        sot._action.assert_called_with(
            self.sess, 'extend', {'grow': {'modifySize': node_count}}
        )
        self.assertIsNone(rt)


class TestExtendClusterNodes(base.TestCase):

    def setUp(self):
        super(TestExtendClusterNodes, self).setUp()

    def test_basic(self):
        sot = cluster.ExtendClusterNodes()

        self.assertEqual(
            '/clusters/%(cluster_id)s/role_extend', sot.base_path
        )
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_patch)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        request = {
            "grow": [
                {"type": "ess-master", "nodesize": 2, "disksize": 0},
                {"type": "ess", "nodesize": 0, "disksize": 60}
            ]
        }
        sot = cluster.ExtendClusterNodes(**request)
        self.assertEqual(request['grow'], sot.grow)
