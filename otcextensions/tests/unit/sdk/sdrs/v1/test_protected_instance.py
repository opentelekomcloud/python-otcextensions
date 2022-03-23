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

from otcextensions.sdk.sdrs.v1 import protected_instance as _protected_instance


EXAMPLE = {
    'id': uuid.uuid4(),
    'name': uuid.uuid4(),
    'description': uuid.uuid4(),
    'server_group_id': uuid.uuid4(),
    'status': 'protected',
    'progress': 0,
    'source_server': uuid.uuid4(),
    'target_server': uuid.uuid4(),
    'created_at': '2022-02-26 20:39:30.718',
    'updated_at': '2022-02-26 21:02:45.507',
    'priority_station': 'source',
    'attachment': [
        {
            'replication': uuid.uuid4(),
            'device': uuid.uuid4()
        }
    ],
    'tags': [
        {
            'key': uuid.uuid4(),
            'value': uuid.uuid4()
        }
    ],
    'metadata': {
        '__system__frozen': False
    }
}


class TestProtectedInstance(base.TestCase):

    def setUp(self):
        super(TestProtectedInstance, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _protected_instance.ProtectedInstance()

    def test_basic(self):
        sot = _protected_instance.ProtectedInstance()
        self.assertEqual('protected_instance', sot.resource_key)
        self.assertEqual('protected_instances', sot.resources_key)
        self.assertEqual('/protected-instances',
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
            'protected_instance_ids': 'protected_instance_ids',
            'query_type': 'query_type',
            'server_group_id': 'server_group_id',
            'server_group_ids': 'server_group_ids',
            'status': 'status'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        test_protected_instance = \
            _protected_instance.ProtectedInstance(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['id'],
            test_protected_instance.id)
        self.assertEqual(
            EXAMPLE['name'],
            test_protected_instance.name)
        self.assertEqual(
            EXAMPLE['description'],
            test_protected_instance.description)
        self.assertEqual(
            EXAMPLE['server_group_id'],
            test_protected_instance.server_group_id)
        self.assertEqual(
            EXAMPLE['status'],
            test_protected_instance.status)
        self.assertEqual(
            EXAMPLE['progress'],
            test_protected_instance.progress)
        self.assertEqual(
            EXAMPLE['source_server'],
            test_protected_instance.source_server)
        self.assertEqual(
            EXAMPLE['target_server'],
            test_protected_instance.target_server)
        self.assertEqual(
            EXAMPLE['created_at'],
            test_protected_instance.created_at)
        self.assertEqual(
            EXAMPLE['updated_at'],
            test_protected_instance.updated_at)
        self.assertEqual(
            EXAMPLE['priority_station'],
            test_protected_instance.priority_station)
        self.assertEqual(
            EXAMPLE['attachment'][0]['replication'],
            test_protected_instance.attachment[0].replication)
        self.assertEqual(
            EXAMPLE['attachment'][0]['device'],
            test_protected_instance.attachment[0].device)
        self.assertEqual(
            EXAMPLE['tags'][0]['key'],
            test_protected_instance.tags[0].key)
        self.assertEqual(
            EXAMPLE['tags'][0]['value'],
            test_protected_instance.tags[0].value)
        self.assertEqual(
            EXAMPLE['metadata']['__system__frozen'],
            test_protected_instance.metadata.system_frozen)
