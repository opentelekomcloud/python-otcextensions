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
from keystoneauth1 import adapter
import mock
from openstack.tests.unit import base

from otcextensions.sdk.sdrs.v1 import replication_pair as _replication_pair


EXAMPLE = {
    'id': uuid.uuid4(),
    'name': uuid.uuid4(),
    'description': uuid.uuid4(),
    'replication_model': 'hypermetro',
    'status': 'protected',
    'volume_ids': uuid.uuid4(),
    'server_group_id': uuid.uuid4(),
    'priority_station': 'source',
    'progress': 100,
    'replication_status': 'active',
    'fault_level': 0,
    'failure_detail': None,
    'created_at': '2022-03-05 09:29:16.221',
    'updated_at': '2022-03-05 13:27:02.612',
    'record_metadata': {
        'volume_size': 100,
        'volume_type': "SAS",
        'multiattach': False,
        'bootable': False
    },
    'attachment': [
        {
            'protected_instance': uuid.uuid4(),
            'device': '/dev/vda'
        }
    ]
}


class TestProtectedInstance(base.TestCase):

    def setUp(self):
        super(TestProtectedInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _replication_pair.ReplicationPair()

    def test_basic(self):
        sot = _replication_pair.ReplicationPair()
        self.assertEqual('replication', sot.resource_key)
        self.assertEqual('replications', sot.resources_key)
        self.assertEqual('/replications',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertDictEqual({
            'availability_zone': 'availability_zone',
            'limit': 'limit',
            'marker': 'marker',
            'name': 'name',
            'offset': 'offset',
            'protected_instance_id': 'protected_instance_id',
            'protected_instance_ids': 'protected_instance_ids',
            'query_type': 'query_type',
            'server_group_id': 'server_group_id',
            'server_group_ids': 'server_group_ids',
            'status': 'status'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        test_replication_pair = _replication_pair.ReplicationPair(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['id'],
            test_replication_pair.id)
        self.assertEqual(
            EXAMPLE['name'],
            test_replication_pair.name)
        self.assertEqual(
            EXAMPLE['description'],
            test_replication_pair.description)
        self.assertEqual(
            EXAMPLE['replication_model'],
            test_replication_pair.replication_model)
        self.assertEqual(
            EXAMPLE['status'],
            test_replication_pair.status)
        self.assertEqual(
            EXAMPLE['volume_ids'],
            test_replication_pair.volume_ids)
        self.assertEqual(
            EXAMPLE['server_group_id'],
            test_replication_pair.server_group_id)
        self.assertEqual(
            EXAMPLE['priority_station'],
            test_replication_pair.priority_station)
        self.assertEqual(
            EXAMPLE['progress'],
            test_replication_pair.progress)
        self.assertEqual(
            EXAMPLE['replication_status'],
            test_replication_pair.replication_status)
        self.assertEqual(
            EXAMPLE['fault_level'],
            test_replication_pair.fault_level)
        self.assertEqual(
            EXAMPLE['failure_detail'],
            test_replication_pair.failure_detail)
        self.assertEqual(
            EXAMPLE['created_at'],
            test_replication_pair.created_at)
        self.assertEqual(
            EXAMPLE['updated_at'],
            test_replication_pair.updated_at)
        self.assertEqual(
            EXAMPLE['record_metadata']['volume_size'],
            test_replication_pair.record_metadata.volume_size)
        self.assertEqual(
            EXAMPLE['record_metadata']['volume_type'],
            test_replication_pair.record_metadata.volume_type)
        self.assertEqual(
            EXAMPLE['record_metadata']['multiattach'],
            test_replication_pair.record_metadata.multiattach)
        self.assertEqual(
            EXAMPLE['record_metadata']['bootable'],
            test_replication_pair.record_metadata.bootable)
        self.assertEqual(
            EXAMPLE['attachment'][0]['protected_instance'],
            test_replication_pair.attachment[0].protected_instance)
        self.assertEqual(
            EXAMPLE['attachment'][0]['device'],
            test_replication_pair.attachment[0].device)
