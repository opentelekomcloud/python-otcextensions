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

from otcextensions.sdk.volume_backup.v2 import backup_policy as _backup_policy
from otcextensions.tests.functional.sdk.volume_backup import TestVbs


def create_backup_policy(client, name):
    data = {
        "name": name,
        "scheduled_policy": {
            "remain_first_backup_of_curMonth": 'Y',
            "rentention_num": 10,
            "frequency": 1,
            "start_time": "12:00",
            "status": "ON"
        }
    }
    return client.create_backup_policy(**data)


class TestBackupPolicy(TestVbs):
    BACKUP_POLICY_NAME = "SDK-" + uuid.uuid4().hex
    policy = None
    volume = None

    def setUp(cls):
        super(TestBackupPolicy, cls).setUp()
        # for volume in cls.conn.block_store.volumes(limit=1):
        #     cls.volume = volume
        #     break
        # if not cls.volume:
        #     raise Exception("no exists volume for test")
        # create backup policy
        cls.policy = create_backup_policy(cls.client, cls.BACKUP_POLICY_NAME)

    def tearDown(cls):
        #: delete backup policy
        if cls.policy and cls.volume:
            cls.conn.volume_backup.unlink_resources_of_policy(cls.policy,
                                                              [cls.volume.id])
        if cls.policy:
            cls.conn.volume_backup.delete_backup_policy(cls.policy)

    def test_list_policies(self):
        policies = list(self.client.backup_policies())
        self.assertGreaterEqual(len(policies), 0)

    def test_find_policy(self):
        policy = self.client.find_backup_policy(self.policy)
        assert isinstance(policy, _backup_policy.BackupPolicy)

        # retest passing only name
        policy = self.client.find_backup_policy(self.policy.name)
        assert isinstance(policy, _backup_policy.BackupPolicy)

    def test_enable_policy(self):
        policy = self.client.enable_policy(self.policy)
        assert isinstance(policy, _backup_policy.BackupPolicy)
        self.assertEqual(policy.scheduled_policy.status, 'ON')

    def test_disable_policy(self):
        policy = self.client.disable_policy(self.policy)
        assert isinstance(policy, _backup_policy.BackupPolicy)
        self.assertEqual(policy.scheduled_policy.status, 'OFF')

    def test_execute_policy(self):
        policy = self.client.enable_policy(self.policy)
        self.client.execute_policy(policy)
