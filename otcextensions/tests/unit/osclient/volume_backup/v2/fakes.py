#   Copyright 2013 Nebula Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
import random
import uuid

import mock

from otcextensions.sdk.volume_backup.v2 import backup_policy

from otcextensions.tests.unit.osclient import test_base


class TestVolumeBackup(test_base.TestCommand):

    def setUp(self):
        super(TestVolumeBackup, self).setUp()

        self.app.client_manager.volume_backup = mock.Mock()
        self.client = self.app.client_manager.volume_backup


class FakePolicy(test_base.Fake):
    """Fake one or more VBS Policy"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'name': 'name-' + uuid.uuid4().hex,
            'policy_resource_count': random.randint(0, 20),
            'tags': [{'key': 't1', 'value': uuid.uuid4().hex}],
            'scheduled_policy': {
                'remain_first_backup_of_curMonth': 'Y',
                'rentention_num': random.randint(0, 100),
                'frequency': random.randint(0, 100),
                'start_time': 'st-' + uuid.uuid4().hex,
                'status': 'ON'
            },
        }
        obj = backup_policy.BackupPolicy.existing(**object_info)
        return obj
