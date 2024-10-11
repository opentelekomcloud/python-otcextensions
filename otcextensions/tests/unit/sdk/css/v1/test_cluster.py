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

from openstack.tests.unit import base
from otcextensions.sdk.css.v1 import cluster
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal


CLUSTER_ID = uuid.uuid4().hex

EXAMPLE = {
    'actionProgress': {},
    'actions': [],
    'authorityEnable': False,
    'backupAvailable': False,
    'bandwidthSize': 0,
    'created': '2024-04-02T23:23:31',
    'cmk_id': 'cmk-id',
    'datastore': {'type': 'elasticsearch', 'version': '7.10.2'},
    'diskEncrypted': False,
    'elbWhiteList': {'whiteList': '', 'enableWhiteList': False},
    'endpoint': [
        '192.168.0.194:9200',
        '192.168.0.12:9200',
        '192.168.0.66:9200',
    ],
    'enterpriseProjectId': '0',
    'httpsEnable': False,
    'id': CLUSTER_ID,
    'instances': [
        {
            'azCode': 'eu-de-01',
            'id': 'node-id',
            'ip': '192.168.0.194',
            'name': 'test-cluster-ess-esn-1-1',
            'specCode': 'css.xlarge.2',
            'status': '200',
            'type': 'ess',
            'volume': {
                'type': 'COMMON',
                'size': 100,
            },
        },
    ],
    'name': 'test-cluster',
    'period': False,
    'publicIp': None,
    'publicKibanaResp': None,
    'securityGroupId': 'sg-id',
    'status': '200',
    'subnetId': 'network-id',
    'tags': [
        {'key': 'key0', 'value': 'value0'},
        {'key': 'key1', 'value': 'value1'},
    ],
    'updated': '2024-04-03T10:37:44',
    'vpcId': 'router-id',
}


EXAMPLE_CREATE = {
    'name': 'test-cluster',
    'datastore': {'type': 'elasticsearch', 'version': '7.10.2'},
    'instanceNum': 3,
    'httpsEnable': False,
    'diskEncryption': {
        'systemEncrypted': '1',
        'systemCmkid': 'cmk-id',
    },
    'instance': {
        'availability_zone': 'eu-de-01',
        'flavorRef': 'css.xlarge.2',
        'volume': {'volume_type': 'COMMON', 'size': 100},
        'nics': {
            'vpcId': 'vpc-id',
            'netId': 'net-id',
            'securityGroupId': 'sg-id',
        },
    },
    'tags': [
        {'key': 'key0', 'value': 'value0'},
        {'key': 'key1', 'value': 'value1'},
    ],
    'backupStrategy': {
        'period': '00:00 GMT+03:00',
        'prefix': 'backup',
        'keepday': 1,
        'bucket': 'css-test-0',
        'agency': 'test-css',
        'basePath': 'css',
    },
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
        self.assertDictEqual(
            {'start': 'start', 'limit': 'limit', 'marker': 'marker'},
            sot._query_mapping._mapping,
        )

    def test_make_it(self):
        sot = cluster.Cluster(**EXAMPLE)
        updated_sot_attrs = {
            'actionProgress': 'action_progress',
            'authorityEnable': 'is_authority_enabled',
            'backupAvailable': 'is_backup_enabled',
            'backupStrategy': 'backup_strategy',
            'bandwidthSize': 'bandwidth_size',
            'created': 'created_at',
            'diskEncrypted': 'is_disk_encrypted',
            'httpsEnable': 'is_https_enabled',
            'period': 'is_billed',
            'publicIp': 'floating_ip',
            'publicKibanaResp': 'public_kibana_resp',
            'securityGroupId': 'security_group_id',
            'subnetId': 'network_id',
            'updated': 'updated_at',
            'vpcId': 'router_id',
            'endpoint': 'endpoints',
            'enterpriseProjectId': 'enterprise_project_id',
            'diskEncryption': 'disk_encryption',
        }

        for key, value in EXAMPLE.items():
            if key in updated_sot_attrs.keys():
                self.assertEqual(getattr(sot, updated_sot_attrs[key]), value)
            elif key == 'instances':
                pass
            elif key == 'elbWhiteList':
                self.assertEqual(
                    sot.elb_whitelist.is_whitelist_enabled,
                    value['enableWhiteList'],
                )
                self.assertEqual(
                    sot.elb_whitelist.whitelist, value['whiteList']
                )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)

        for i in range(len(sot.nodes)):
            instance = EXAMPLE['instances'][i]
            self.assertEqual(
                instance['azCode'], sot.nodes[i].availability_zone
            )
            self.assertEqual(sot.nodes[i].id, instance['id'])
            self.assertEqual(sot.nodes[i].ip, instance['ip'])
            self.assertEqual(sot.nodes[i].name, instance['name'])
            self.assertEqual(sot.nodes[i].flavor, instance['specCode'])
            self.assertEqual(sot.nodes[i].status, instance['status'])
            self.assertEqual(sot.nodes[i].type, instance['type'])
            assert_attributes_equal(
                self, sot.nodes[i].volume, instance['volume']
            )

    def test_create_sot(self):
        updated_sot_attrs = {
            'instanceNum': 'instance_num',
            'httpsEnable': 'is_https_enabled',
        }
        sot = cluster.Cluster(**EXAMPLE_CREATE)
        for key, value in EXAMPLE_CREATE.items():
            if key in updated_sot_attrs.keys():
                self.assertEqual(getattr(sot, updated_sot_attrs[key]), value)
            elif key == 'diskEncryption':
                self.assertEqual(
                    sot.disk_encryption.system_encrypted,
                    value['systemEncrypted'],
                )
                self.assertEqual(
                    sot.disk_encryption.system_cmkid, value['systemCmkid']
                )
            elif key == 'instance':
                self.assertEqual(
                    sot.instance.nics.network_id, value['nics']['netId']
                )
                self.assertEqual(
                    sot.instance.nics.router_id, value['nics']['vpcId']
                )
                self.assertEqual(
                    sot.instance.nics.security_group_id,
                    value['nics']['securityGroupId'],
                )
                self.assertEqual(sot.instance.flavor, value.pop('flavorRef'))
                del value['nics']
                assert_attributes_equal(self, sot.instance, value)
            elif key == 'backupStrategy':
                self.assertEqual(
                    sot.backup_strategy.base_path, value.pop('basePath')
                )
                assert_attributes_equal(self, sot.backup_strategy, value)
            else:
                assert_attributes_equal(self, getattr(sot, key), value)

    def test_action(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        action = 'restart'
        json_body = {'restart': {}}
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        self.sess.post.return_value = response

        rt = sot._action(self.sess, action, json_body)
        self.sess.post.assert_called_with(
            'clusters/%s/restart' % sot.id, json=json_body
        )

        self.assertIsNone(rt)

    def test_restart(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()

        rt = sot.restart(self.sess)
        sot._action.assert_called_with(self.sess, 'restart')
        self.assertIsNone(rt)

    def test_extend(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        node_count = 3

        rt = sot.extend(self.sess, node_count)
        sot._action.assert_called_with(
            self.sess, 'extend', {'grow': {'modifySize': node_count}}
        )
        self.assertIsNone(rt)

    def test_update_name(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        new_name = 'test_update_name'

        body = {'displayName': new_name}

        rt = sot.update_name(self.sess, new_name)
        sot._action.assert_called_with(self.sess, 'changename', body)
        self.assertIsNone(rt)

    def test_update_password(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        new_password = 'test_new_123_Pass'

        body = {'newpassword': new_password}

        rt = sot.update_password(self.sess, new_password)
        sot._action.assert_called_with(self.sess, 'password/reset', body)
        self.assertIsNone(rt)

    def test_update_security_mode(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()

        authority_enable = True
        https_enable = True
        admin_pwd = None

        body = {
            'authorityEnable': authority_enable,
            'httpsEnable': https_enable,
        }

        rt1 = sot.update_security_mode(
            self.sess, https_enable, authority_enable, admin_pwd
        )
        sot._action.assert_called_with(self.sess, 'mode/change', body)
        self.assertIsNone(rt1)

        admin_pwd = 'new_Pass_123'
        body['adminPwd'] = admin_pwd

        rt2 = sot.update_security_mode(
            self.sess, https_enable, authority_enable, admin_pwd
        )
        sot._action.assert_called_with(self.sess, 'mode/change', body)
        self.assertIsNone(rt2)

    def test_update_security_group(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        security_group_id = 'test_security_group_id'

        body = {'security_group_ids': security_group_id}

        rt = sot.update_security_group(self.sess, security_group_id)
        sot._action.assert_called_with(self.sess, 'sg/change', body)
        self.assertIsNone(rt)

    def test_update_kernel(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()

        target_image_id = 'target_image_id'
        upgrade_type = 'same'
        indices_backup_check = True
        agency = 'test-agency'

        body = {
            'target_image_id': target_image_id,
            'upgrade_type': upgrade_type,
            'indices_backup_check': indices_backup_check,
            'agency': agency,
            'cluster_load_check': True,
        }

        rt1 = sot.update_kernel(
            self.sess,
            target_image_id,
            upgrade_type,
            indices_backup_check,
            agency,
        )
        sot._action.assert_called_with(
            self.sess, 'inst-type/all/image/upgrade', body
        )
        self.assertIsNone(rt1)

    def test_update_flavor(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        new_flavor = 'test_update_name'
        body = {'needCheckReplica': True, 'newFlavorId': new_flavor}

        rt1 = sot.update_flavor(self.sess, new_flavor, check_replica=True)
        sot._action.assert_called_with(self.sess, 'flavor', body)
        self.assertIsNone(rt1)

        rt2 = sot.update_flavor(
            self.sess, new_flavor, node_type='ess', check_replica=True
        )
        sot._action.assert_called_with(self.sess, 'ess/flavor', body)
        self.assertIsNone(rt2)

    def test_scale_in(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        nodes = ['5e134b90-8159-4333-9dae-4305029a838a']

        body = {
            'shrinkNodes': nodes,
        }

        rt = sot.scale_in(self.sess, nodes)
        sot._action.assert_called_with(self.sess, 'node/offline', body)
        self.assertIsNone(rt)

    def test_scale_in_by_node_type(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()
        nodes = [{'type': 'ess', 'reducedNodeNum': 1}]

        body = {'shrink': nodes}

        rt = sot.scale_in_by_node_type(self.sess, nodes)
        sot._action.assert_called_with(self.sess, 'role/shrink', body)
        self.assertIsNone(rt)

    def test_replace_node(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        node_id = 'test-id'
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        self.sess.put.return_value = response

        rt = sot.replace_node(self.sess, node_id)
        self.sess.put.assert_called_with(
            f'clusters/{sot.id}/instance/{node_id}/replace'
        )

        self.assertIsNone(rt)

    def test_add_nodes(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        sot._action = mock.Mock()

        node_type = 'ess-client'
        flavor = 'flavor-id'
        node_size = 3
        volume_type = 'volume-type'
        body = {
            'type': {
                'flavor_ref': flavor,
                'node_size': node_size,
                'volume_type': volume_type,
            }
        }

        rt = sot.add_nodes(
            self.sess, node_type, flavor, node_size, volume_type
        )
        sot._action.assert_called_with(
            self.sess, f'type/{node_type}/independent', body
        )
        self.assertIsNone(rt)

    def test_retry_upgrade_job(self):
        sot = cluster.Cluster.existing(id=CLUSTER_ID)
        job_id = 'action-id'
        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        self.sess.put.return_value = response

        rt1 = sot.retry_upgrade_job(self.sess, job_id)
        self.sess.put.assert_called_with(
            f'clusters/{sot.id}/upgrade/{job_id}/retry', params={}
        )

        self.assertIsNone(rt1)

        retry_mode = 'abort'
        rt2 = sot.retry_upgrade_job(self.sess, job_id, retry_mode)
        self.sess.put.assert_called_with(
            f'clusters/{sot.id}/upgrade/{job_id}/retry',
            params={'retry_mode': retry_mode},
        )

        self.assertIsNone(rt2)


class TestExtendClusterNodes(base.TestCase):
    def setUp(self):
        super(TestExtendClusterNodes, self).setUp()

    def test_basic(self):
        sot = cluster.ExtendClusterNodes()

        self.assertEqual('/clusters/%(cluster_id)s/role_extend', sot.base_path)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_delete)
        self.assertFalse(sot.allow_patch)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        request = {
            'grow': [
                {'type': 'ess-master', 'nodesize': 2, 'disksize': 0},
                {'type': 'ess', 'nodesize': 0, 'disksize': 60},
            ]
        }
        sot = cluster.ExtendClusterNodes(**request)
        self.assertEqual(request['grow'], sot.grow)
