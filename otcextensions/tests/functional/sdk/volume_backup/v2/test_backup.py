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

from openstack import resource

# from otcextensions.sdk.volume_backup.v2 import backup as _backup
from otcextensions.tests.functional.sdk.volume_backup import TestVbs


class TestBackup(TestVbs):
    BACKUP_NAME = "SDK-" + uuid.uuid4().hex
    volume = None
    job = None

    @classmethod
    def setUpClass(cls):
        super(TestBackup, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    def prepare_volume(self):

        self.SNAPSHOT_NAME = self.getUniqueString()
        self.SNAPSHOT_ID = None
        self.VOLUME_NAME = self.getUniqueString()
        self.VOLUME_ID = None

        volume = self.conn.block_storage.create_volume(
            name=self.VOLUME_NAME,
            size=1)
        resource.wait_for_status(
            session=self.conn.block_storage,
            resource=volume,
            status='available',
            failures=['error'],
            interval=2,
            wait=120)
        # assert isinstance(volume, _volume.Volume)
        self.assertEqual(self.VOLUME_NAME, volume.name)
        self.VOLUME_ID = volume.id
        snapshot = self.conn.block_storage.create_snapshot(
            name=self.SNAPSHOT_NAME,
            volume_id=self.VOLUME_ID)
        resource.wait_for_status(
            session=self.conn.block_storage,
            resource=snapshot,
            status='available',
            failures=['error'],
            interval=2,
            wait=120)
        # assert isinstance(snapshot, _snapshot.Snapshot)
        self.assertEqual(self.SNAPSHOT_NAME, snapshot.name)
        self.SNAPSHOT_ID = snapshot.id

    def cleanup_volume(self):
        snapshot = self.conn.block_storage.get_snapshot(self.SNAPSHOT_ID)
        sot = self.conn.block_storage.delete_snapshot(
            snapshot, ignore_missing=False)
        self.conn.block_storage.wait_for_delete(
            snapshot, interval=2, wait=120)
        self.assertIsNone(sot)
        sot = self.conn.block_storage.delete_volume(
            self.VOLUME_ID, ignore_missing=False)
        self.assertIsNone(sot)

    def test_list_backup(self):
        query = {}
        backups = list(self.client.backups(**query))
        self.assertGreaterEqual(len(backups), 0)

    def test_list_backup_details(self):
        query = {}
        backups = list(self.client.backups(details=True, **query))
        self.assertGreaterEqual(len(backups), 0)

    def test_list_backup_pagination(self):
        query = {}
        backups = list(self.client.backups(**query))
        self.assertGreaterEqual(len(backups), 0)
        query['limit'] = 1
        backups_new = list(self.client.backups(**query))
        self.assertGreaterEqual(len(backups), len(backups_new))

    def test_list_backup_filter_status(self):
        query = {
            'status': 'available'
        }
        backups = list(self.client.backups(details=True, **query))
        if len(backups) > 0:
            for backup in backups:
                self.assertEqual(backup.status, 'available')

    def test_get_backup_from_detail(self):
        query = {}
        backups = list(self.client.backups(details=True, **query))
        if len(backups) > 0:
            backup = self.client.get_backup(backups[0])
            self.assertIsNotNone(backup)

    def test_get_backup(self):
        query = {}
        backups = list(self.client.backups(**query))
        if len(backups) > 0:
            backup = self.client.get_backup(backups[0])
            self.assertIsNotNone(backup)

    # TODO(AGoncharov) backup creation takes too long.
    # 1Gb empty volume backup takes more than 4 min
    # The functional test for create/delete can not be scheduled with such
    # timing
    # def test_create_delete_backup(self):
    #     self.prepare_volume()
    #
    #     backup = self.client.create_backup(
    #         volume_id=self.VOLUME_ID,
    #         snapshot_id=self.SNAPSHOT_ID,
    #         name='sdk_test_backup')
    #     assert isinstance(backup, _backup.Backup)
    #     self.client.wait_for_backup(backup)
    #     self.client.delete_backup(backup)
    #     self.client.wait_for_backup_delete(backup)
    #     self.cleanup_volume()
