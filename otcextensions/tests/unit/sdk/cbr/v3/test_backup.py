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

from otcextensions.sdk.cbr.v3 import backup as _backup


EXAMPLE = {
    'provider_id': uuid.uuid4(),
    'checkpoint_id': uuid.uuid4(),
    'updated_at': '2020-02-21T07:07:25.113761',
    'vault_id': uuid.uuid4(),
    'id': uuid.uuid4(),
    'resource_az': 'eu-de-01',
    'image_type': 'backup',
    'resource_id': uuid.uuid4(),
    'resource_size': 40,
    'children': [],
    'extend_info': {
        'auto_trigger': True,
        'supported_restore_mode': 'backup',
        'contain_system_disk': True,
        'support_lld': True,
        'architecture': 'x86_64',
        'system_disk': False,
        'app_consistency': {
            'error_code': '0',
            'error_status': '0',
            'error_message': '',
            'app_consistency': '0'
        }
    },
    'project_id': uuid.uuid4(),
    'status': 'available',
    'resource_name': 'test001-02',
    'description': '',
    'expired_at': '2020-05-21T07:00:54.060493',
    'replication_records': [],
    'name': 'autobk_b629',
    'created_at': '2020-02-21T07:00:54.065135',
    'resource_type': 'OS::Nova::Server'
}


class TestBackup(base.TestCase):

    def setUp(self):
        super(TestBackup, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.delete = mock.Mock()
        self.sess.put = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _backup.Backup()
        self.sot_expected = _backup.Backup(**EXAMPLE)

    def test_basic(self):
        sot = _backup.Backup()
        self.assertEqual('backup', sot.resource_key)
        self.assertEqual('backups', sot.resources_key)
        self.assertEqual('/backups',
                         sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)
        self.assertDictEqual({
            'checkpoint_id': 'checkpoint_id',
            'dec': 'dec',
            'end_time': 'end_time',
            'enterprise_project_id': 'enterprise_project_id',
            'image_type': 'image_type',
            'limit': 'limit',
            'marker': 'marker',
            'member_status': 'member_status',
            'name': 'name',
            'offset': 'offset',
            'own_type': 'own_type',
            'parent_id': 'parent_id',
            'resource_az': 'resource_az',
            'resource_id': 'resource_id',
            'resource_name': 'resource_name',
            'resource_type': 'resource_type',
            'sort': 'sort',
            'start_time': 'start_time',
            'status': 'status',
            'used_percent': 'used_percent',
            'vault_id': 'vault_id'
        }, sot._query_mapping._mapping)

    def test_make_it(self):
        test_backup = _backup.Backup(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['provider_id'],
            test_backup.provider_id)
        self.assertEqual(
            EXAMPLE['checkpoint_id'],
            test_backup.checkpoint_id)
        self.assertEqual(
            EXAMPLE['updated_at'],
            test_backup.updated_at)
        self.assertEqual(
            EXAMPLE['vault_id'],
            test_backup.vault_id)
        self.assertEqual(
            EXAMPLE['id'],
            test_backup.id)
        self.assertEqual(
            EXAMPLE['resource_az'],
            test_backup.resource_az)
        self.assertEqual(
            EXAMPLE['image_type'],
            test_backup.image_type)
        self.assertEqual(
            EXAMPLE['resource_id'],
            test_backup.resource_id)
        self.assertEqual(
            EXAMPLE['resource_size'],
            test_backup.resource_size)
        self.assertEqual(
            EXAMPLE['children'],
            test_backup.children)
        self.assertEqual(
            EXAMPLE['project_id'],
            test_backup.project_id)
        self.assertEqual(
            EXAMPLE['status'],
            test_backup.status)
        self.assertEqual(
            EXAMPLE['resource_name'],
            test_backup.resource_name)
        self.assertEqual(
            EXAMPLE['description'],
            test_backup.description)
        self.assertEqual(
            EXAMPLE['expired_at'],
            test_backup.expired_at)
        self.assertEqual(
            EXAMPLE['replication_records'],
            test_backup.replication_records)
        self.assertEqual(
            EXAMPLE['name'],
            test_backup.name)
        self.assertEqual(
            EXAMPLE['created_at'],
            test_backup.created_at)
        self.assertEqual(
            EXAMPLE['resource_type'],
            test_backup.resource_type)
        self.assertTrue(
            test_backup.extend_info.auto_trigger)
        self.assertEqual(
            EXAMPLE['extend_info']['supported_restore_mode'],
            test_backup.extend_info.supported_restore_mode)
        self.assertTrue(
            test_backup.extend_info.contain_system_disk)
        self.assertTrue(
            test_backup.extend_info.support_lld)
        self.assertEqual(
            EXAMPLE['extend_info']['architecture'],
            test_backup.extend_info.architecture)
        self.assertFalse(
            test_backup.extend_info.system_disk)
        self.assertEqual(
            EXAMPLE['extend_info']['app_consistency']['app_consistency'],
            test_backup.extend_info.app_consistency.app_consistency)
        self.assertEqual(
            EXAMPLE['extend_info']['app_consistency']['error_code'],
            test_backup.extend_info.app_consistency.error_code)
        self.assertEqual(
            EXAMPLE['extend_info']['app_consistency']['error_message'],
            test_backup.extend_info.app_consistency.error_message)
        self.assertEqual(
            EXAMPLE['extend_info']['app_consistency']['error_status'],
            test_backup.extend_info.app_consistency.error_status)
