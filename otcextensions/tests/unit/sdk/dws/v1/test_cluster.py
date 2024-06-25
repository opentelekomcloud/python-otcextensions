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
from otcextensions.sdk.dws.v1 import cluster

EXAMPLE = {
    'action_progress': {},
    'availability_zone': 'eu-de-01',
    'created': '2023-01-16T02:11:19',
    # "elb": None,
    'endpoints': [
        {
            'connect_info': 'test-dws-6433a577.dws.otc-tsi.de',
            'jdbc_url': 'jdbc:postgresql://test.example.com:8000/gaussdb',
        }
    ],
    'enterprise_project_id': uuid.uuid4().hex,
    'guest_agent_version': '8.1.1.202',
    'id': uuid.uuid4().hex,
    'logical_cluster_initialed': False,
    'logical_cluster_mode': False,
    'maintain_window': {
        'day': 'Thu',
        'end_time': '02:00',
        'start_time': '22:00',
    },
    'name': 'test-dws-6433a577',
    'node_type': 'dws.m3.xlarge',
    'node_type_id': uuid.uuid4().hex,
    'nodes': [
        {'id': uuid.uuid4().hex, 'status': '200'},
        {'id': uuid.uuid4().hex, 'status': '200'},
        {'id': uuid.uuid4().hex, 'status': '200'},
    ],
    'number_of_free_node': 0,
    'number_of_node': 6,
    'parameter_group': {
        'id': uuid.uuid4().hex,
        'name': 'parameterGroupFor_bd5cdd60-0c94-4f38-9a23-49cb2c5c425a',
        'status': 'In-Sync',
    },
    'plugins': [
        {
            'aarchType': 'x86_64',
            'autoInstall': 'install|upgrade',
            'datastoreType': 'dws',
            'datastoreVersion': '8.1.1.202',
            'id': uuid.uuid4().hex,
            'packageName': '8.1.1.202-dmsAgent-x86_64-20220211161451.tar.gz',
            'status': '0',
            'type': 'dmsAgent',
            'updateTime': 1666792707000,
            'version': '8.1.1.202',
        },
        {
            'aarchType': 'all',
            'autoInstall': 'install|upgrade',
            'datastoreType': 'dws',
            'datastoreVersion': '8.1.1.202',
            'id': uuid.uuid4().hex,
            'packageName': '8.1.1.202-inspect-ed1eb6e-20220207110934.tar.gz',
            'status': '0',
            'type': 'inspect',
            'updateTime': 1666792707000,
            'version': '8.1.1.202',
        },
    ],
    'port': 8000,
    'private_ip': ['192.168.1.192', '192.168.1.15', '192.168.1.73'],
    'public_endpoints': [
        {
            'jdbc_url': 'jdbc:postgresql://test.example.com:8000/gaussdb',
            'public_connect_info': 'test.example.com',
        }
    ],
    'public_ip': {
        'eip_address': '80.158.89.54',
        'eip_id': uuid.uuid4().hex,
        'public_bind_type': 'auto_assign',
    },
    'recent_event': 9,
    'security_group_id': uuid.uuid4().hex,
    'spec_version': 'v1.0',
    'status': 'AVAILABLE',
    'sub_status': 'NORMAL',
    'subnet_id': uuid.uuid4().hex,
    'tags': [
        {'key': 'key1', 'value': 'value1'},
        {'key': 'key2', 'value': 'value2'},
    ],
    'task_status': 'SNAPSHOTTING',
    'updated': '2023-01-16T02:11:19',
    'use_logical_cluster': False,
    'user_name': 'dbadmin',
    'version': '8.1.1.202',
    'vpc_id': uuid.uuid4().hex,
    'failed_reasons': {},
}


class TestCluster(base.TestCase):
    def setUp(self):
        super(TestCluster, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = cluster.Cluster()

        self.assertEqual('/clusters', sot.base_path)
        self.assertEqual('clusters', sot.resources_key)
        self.assertEqual('cluster', sot.resource_key)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = cluster.Cluster(**EXAMPLE)
        updated_sot_attrs = (
            'vpc_id',
            'subnet_id',
            'node_type',
            'node_type_id',
            'public_ip',
            'updated',
            'created',
            'failed_reasons',
            'use_logical_cluster',
            'logical_cluster_initialed',
            'logical_cluster_mode',
            'logical_cluster_mode',
            'maintain_window',
            'number_of_free_node',
            'number_of_node',
            'recent_event',
        )

        self.assertEqual(EXAMPLE['vpc_id'], sot.router_id)
        self.assertEqual(EXAMPLE['subnet_id'], sot.network_id)
        self.assertEqual(EXAMPLE['node_type'], sot.flavor)
        self.assertEqual(EXAMPLE['node_type_id'], sot.flavor_id)

        self.assertEqual(EXAMPLE['public_ip'], sot.floating_ip)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['updated'], sot.updated_at)
        self.assertEqual(EXAMPLE['failed_reasons'], sot.error)
        self.assertEqual(
            EXAMPLE['use_logical_cluster'], sot.is_logical_cluster_enabled
        )
        self.assertEqual(
            EXAMPLE['logical_cluster_initialed'],
            sot.is_logical_cluster_initialed,
        )
        self.assertEqual(
            EXAMPLE['logical_cluster_mode'], sot.is_logical_cluster_mode
        )
        self.assertEqual(EXAMPLE['maintain_window'], sot.maintenance_window)
        self.assertEqual(EXAMPLE['number_of_free_node'], sot.num_free_nodes)
        self.assertEqual(EXAMPLE['number_of_node'], sot.num_nodes)
        self.assertEqual(EXAMPLE['recent_event'], sot.num_recent_events)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

    def test_action(self):
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
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
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
        sot._action = mock.Mock()

        rt = sot.restart(self.sess)
        sot._action.assert_called_with(self.sess, 'restart', {'restart': {}})
        self.assertIsNone(rt)

    def test_scale_out(self):
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
        sot._action = mock.Mock()
        node_count = 3

        rt = sot.scale_out(self.sess, node_count)
        sot._action.assert_called_with(
            self.sess, 'resize', {'scale_out': {'count': node_count}}
        )
        self.assertIsNone(rt)

    def test_reset_password(self):
        sot = cluster.Cluster.existing(id=EXAMPLE['id'])
        sot._action = mock.Mock()
        new_password = 'TestNewPassword'

        rt = sot.reset_password(self.sess, new_password)
        sot._action.assert_called_with(
            self.sess, 'reset-password', {'new_password': new_password}
        )
        self.assertIsNone(rt)
