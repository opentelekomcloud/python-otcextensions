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

from otcextensions.sdk.rds.v3 import backup

IDENTIFIER = 'IDENTIFIER'
EXAMPLE = {
    'id': IDENTIFIER,
    'name': '50deafb3e45d451a9406ca146b71fe9a_rds',
    'description': '',
    'begin_time': '2016-08-23T04:01:40',
    'end_time': '2016-08-23T04:04:40',
    'status': 'COMPLETED',
    'instance_id': '4f87d3c4-9e33-482f-b962-e23b30d1a18c',
    'type': 'manual',
    'datastore': {}
}

EXAMPLE_POLICY = {
    'keep_days': 7,
    'start_time': '00:00:00',
    'period': '1,2'
}

EXAMPLE_FILE = {
    'name': '43e4feaab48f11e89039fa163ebaa7e4br01.xxx',
    'size': 2803,
    'download_link': 'fake_url',
    'link_expired_time': '2018-08-016T10:15:14+0800'
}


class TestBackup(base.TestCase):

    def test_basic(self):
        sot = backup.Backup()
        self.assertIsNone(sot.resource_key)
        self.assertEqual('backups', sot.resources_key)
        self.assertEqual('/backups', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertFalse(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = backup.Backup(**EXAMPLE)
        self.assertEqual(IDENTIFIER, sot.id)
        self.assertEqual(EXAMPLE['name'], sot.name)
        self.assertEqual(EXAMPLE['instance_id'], sot.instance_id)
        self.assertEqual(EXAMPLE['description'], sot.description)
        self.assertEqual(EXAMPLE['begin_time'], sot.begin_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['type'], sot.type)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['datastore'], sot.datastore)


class TestBackupPolicy(base.TestCase):

    def test_basic(self):
        sot = backup.BackupPolicy()
        self.assertIsNone(sot.resources_key)
        self.assertEqual('backup_policy', sot.resource_key)

        self.assertEqual('/instances/%(instance_id)s/backups/policy',
                         sot.base_path)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.requires_id)

    def test_make_it(self):
        sot = backup.BackupPolicy(**EXAMPLE_POLICY)
        self.assertEqual(EXAMPLE_POLICY['keep_days'], sot.keep_days)
        self.assertEqual(EXAMPLE_POLICY['start_time'], sot.start_time)
        self.assertEqual(EXAMPLE_POLICY['period'], sot.period)


class TestBackupFile(base.TestCase):

    def test_basic(self):
        sot = backup.BackupFile()
        self.assertEqual('files', sot.resources_key)
        self.assertEqual('/backup-files', sot.base_path)
        self.assertTrue(sot.allow_list)

        self.assertDictEqual({
            'limit': 'limit',
            'marker': 'marker',
            'backup_id': 'backup_id'},
            sot._query_mapping._mapping)

    def test_make_it(self):
        sot = backup.BackupFile(**EXAMPLE_FILE)
        self.assertEqual(EXAMPLE_FILE['name'], sot.name)
        self.assertEqual(EXAMPLE_FILE['size'], sot.size)
        self.assertEqual(EXAMPLE_FILE['download_link'], sot.download_link)
        self.assertEqual(EXAMPLE_FILE['link_expired_time'], sot.expires_at)
