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

import mock

from openstack.tests.unit import base

from otcextensions.sdk.rds.v3 import instance

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    "id": IDENTIFIER,
    "availability_zone": "fake_az",
    "status": "ACTIVE",
    "name": "mysql-0820-022709-01",
    "port": 3306,
    "type": "Single",
    "region": "eu-de",
    "datastore": {
        "type": "mysql",
        "version": "5.7"
    },
    "replica_of_id": "some_fake",
    "created": "2018-08-20T02:33:49+0800",
    "updated": "2018-08-20T02:33:50+0800",
    "volume": {
        "type": "ULTRAHIGH",
        "size": 100
    },
    "ha": {
        "replication_mode": "sync"
    },
    "nodes": [{
        "id": "06f1c2ad57604ae89e153e4d27f4e4b8no01",
        "name": "mysql-0820-022709-01_node0",
        "role": "master",
        "status": "ACTIVE",
        "availability_zone": "eu-de-01"
    }],
    "private_ips": ["192.168.0.142"],
    "public_ips": ["10.154.219.187", "10.154.219.186"],
    "password": "fake_pass",
    "vpc_id": "b21630c1-e7d3-450d-907d-39ef5f445ae7",
    "subnet_id": "45557a98-9e17-4600-8aec-999150bc4eef",
    "security_group_id": "38815c5c-482b-450a-80b6-0a301f2afd97",
    "flavor_ref": "rds.mysql.s1.large",
    "switch_strategy": "",
    "backup_strategy": {
        "start_time": "19:00-20:00",
        "keep_days": 7
    },
    "maintenance_window": "02:00-06:00",
    "related_instance": [],
    "disk_encryption_id": "",
    "time_zone": ""
}


class TestInstance(base.TestCase):
    def setUp(self):
        super(TestInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = None
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        # self.sess.get_project_id = mock.Mock(return_value=PROJECT_ID)
        self.sot = instance.Instance(**EXAMPLE)

    def test_basic(self):
        sot = instance.Instance()
        self.assertIsNone(sot.resource_key)
        self.assertEqual('instances', sot.resources_key)
        self.assertEqual('/instances', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = instance.Instance(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['availability_zone'], sot.availability_zone)
        self.assertEqual(EXAMPLE['backup_strategy'], sot.backup_strategy)
        self.assertEqual(EXAMPLE['created'], sot.created_at)
        self.assertEqual(EXAMPLE['datastore'], sot.datastore)
        self.assertEqual(EXAMPLE['disk_encryption_id'], sot.disk_encryption_id)
        self.assertEqual(EXAMPLE['flavor_ref'], sot.flavor_ref)
        self.assertEqual(EXAMPLE['ha'], sot.ha)
        self.assertEqual(EXAMPLE['nodes'], sot.nodes)
        self.assertEqual(EXAMPLE['password'], sot.password)
        self.assertEqual(EXAMPLE['port'], sot.port)
        self.assertEqual(EXAMPLE['volume'], sot.volume)
        self.assertEqual(EXAMPLE['region'], sot.region)
        self.assertEqual(EXAMPLE['port'], sot.port)
        self.assertEqual(EXAMPLE['private_ips'], sot.private_ips)
        self.assertEqual(EXAMPLE['public_ips'], sot.public_ips)
        self.assertEqual(EXAMPLE['region'], sot.region)
        self.assertEqual(EXAMPLE['related_instance'], sot.related_instances)
        self.assertEqual(EXAMPLE['replica_of_id'], sot.replica_of_id)
        self.assertEqual(EXAMPLE['vpc_id'], sot.router_id)
        self.assertEqual(EXAMPLE['security_group_id'], sot.security_group_id)
        self.assertEqual(EXAMPLE['subnet_id'], sot.subnet_id)
        self.assertEqual(EXAMPLE['switch_strategy'], sot.switch_strategy)
        self.assertEqual(EXAMPLE['maintenance_window'], sot.maintenance_window)
        self.assertEqual(EXAMPLE['time_zone'], sot.time_zone)

    def test_fetch_restore_times(self):
        sot = instance.Instance(**EXAMPLE)
        restore_times = [{
            'start_time': 'some_start_time',
            'end_time': 'some_end_time'
        }]
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {
            'restore_time': restore_times}
        response.headers = {}
        self.sess.get.return_value = response

        rt = sot.fetch_restore_times(self.sess)

        self.assertEqual(restore_times, rt)
        self.assertEqual(restore_times, sot.restore_time)

    def test_fetch(self):
        sot = instance.Instance.existing(id=IDENTIFIER)

        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {'instances': [EXAMPLE]}
        response.headers = {}
        self.sess.get.return_value = response

        # Restore from backup
        rt = sot.fetch(self.sess)
        self.assertIsInstance(rt, instance.Instance)
        self.assertDictEqual(
            rt.to_dict(),
            instance.Instance(**EXAMPLE)
        )

    def test_restore(self):
        sot = instance.Instance(**EXAMPLE)
        job_id = 'fake_job'

        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {'job_id': job_id}
        response.headers = {}
        self.sess.post.return_value = response

        class FakeResource(object):
            def __init__(self, id):
                self.id = id

        # Restore from backup
        rt = sot.restore(self.sess, FakeResource('bid'))

        self.sess.post.assert_called_with(
            'instances/recovery',
            json={
                'source': {
                    'type': 'backup', 'backup_id': 'bid',
                    'instance_id': IDENTIFIER},
                'target': {'instance_id': IDENTIFIER}})

        # PIT
        rt = sot.restore(self.sess, None, 'rit')

        self.sess.post.assert_called_with(
            'instances/recovery',
            json={
                'source': {
                    'type': 'timestamp', 'restore_time': 'rit',
                    'instance_id': IDENTIFIER},
                'target': {'instance_id': IDENTIFIER}})

        self.assertEqual(job_id, rt)

    def test_get_backup_policy(self):
        sot = instance.Instance(**EXAMPLE)
        backup_policy = {
            'keep_days': 7,
            'start_time': '19:00-20:00',
            'period': '1,2'
        }
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = {
            'backup_policy': backup_policy}
        response.headers = {}
        self.sess.get.return_value = response

        rt = sot.get_backup_policy(self.sess)

        self.sess.get.assert_called_with('instances/IDENTIFIER/backups/policy')

        self.assertEqual(backup_policy, rt)

    def test_set_backup_policy(self):
        sot = instance.Instance(**EXAMPLE)
        backup_policy = {
            'keep_days': 7,
            'start_time': '19:00-20:00',
            'period': '1,2'
        }

        response = mock.Mock()
        response.status_code = 200
        response.headers = {}
        self.sess.put.return_value = response

        rt = sot.set_backup_policy(self.sess, **backup_policy)

        self.sess.put.assert_called_with(
            'instances/IDENTIFIER/backups/policy',
            json={'backup_policy': {'keep_days': 7, 'start_time':
                                    '19:00-20:00', 'period': '1,2'}})

        self.assertIsNone(rt)
