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
import datetime
import random
import uuid

import mock

from otcextensions.sdk.cbr.v3 import checkpoint
from otcextensions.sdk.cbr.v3 import policy
from otcextensions.sdk.cbr.v3 import task
from otcextensions.sdk.cbr.v3 import vault
from otcextensions.tests.unit.osclient import test_base


def generate_vault_list():
    """Generate random list of vault UUIDs"""
    vault_list = []
    random_int = random.randint(1, 10)
    while random_int > 0:
        vault_list.append({
            'vault_id': uuid.uuid4().hex})
        random_int -= 1
    return vault_list


def generate_pattern():
    pattern = ''
    on_daily_base = random.choice([True, False])
    days = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']
    if on_daily_base:
        pattern = 'FREQ=DAILY;INTERVAL=' + str(random.randint(1, 30)) + ';'
    else:
        pattern = 'FREQ=WEEKLY;BYDAY='
        day_count = random.randint(1, 7)
        day_list = random.sample(days, day_count)
        day_list_len = len(day_list)
        for item in day_list:
            pattern = pattern + item
            if day_list_len != 1:
                pattern += ','
            else:
                pattern += ';'
            day_list_len -= 1
    byhour = random.randint(0, 23)
    if byhour < 10:
        byhour = 'BYHOUR=' + '0' + str(byhour) + ';'
    else:
        byhour = 'BYHOUR=' + str(byhour) + ';'
    pattern += byhour
    byminute = random.randint(0, 59)
    if byminute < 10:
        byminute = 'BYMINUTE=' + '0' + str(byminute)
    else:
        byminute = 'BYMINUTE=' + str(byminute)
    pattern += byminute
    return pattern


def generate_pattern_list():
    """Generate random list of patterns"""
    pattern_list = []
    random_int = random.randint(1, 5)
    while random_int > 0:
        pattern_list.append(generate_pattern())
        random_int -= 1
    return pattern_list


class TestCBR(test_base.TestCommand):

    def setUp(self):
        super(TestCBR, self).setUp()

        self.app.client_manager.cbr = mock.Mock()
        self.client = self.app.client_manager.cbr


class FakeCheckpoint(test_base.Fake):
    """Fake one or more CBR checkpoint"""

    @classmethod
    def generate(cls):
        object_info = {
            'created_at': uuid.uuid4().hex,
            'id': 'pid-' + uuid.uuid4().hex,
            'status': 'available',
            'name': 'checkpoint-' + uuid.uuid4().hex,
            'vault':
                {
                    'id': uuid.uuid4().hex,
                    'name': uuid.uuid4().hex,
                    "resources": [
                        {
                            'name': 'resource-name-' + uuid.uuid4().hex,
                            'resource_size': '6',
                            'backup_size': '6840',
                            'protect_status': 'available',
                            'backup_count': '18',
                            'type': 'OS::Nova::Server',
                            'id': 'pid-' + uuid.uuid4().hex,
                            'extra_info': '{}'
                        }]
            },
            'extra_info':
                {
                    'name': 'backup-' + uuid.uuid4().hex
            }
        }

        obj = checkpoint.Checkpoint.existing(**object_info)
        return obj


class FakePolicy(test_base.Fake):
    """Fake one or more CBR policies with random vaults list and patterns"""

    @classmethod
    def generate(cls):
        object_info = {
            "name": 'name-' + uuid.uuid4().hex,
            "associated_vaults": generate_vault_list(),
            "enabled": random.choice([True, False]),
            "trigger": {
                "properties": {
                    "pattern": generate_pattern_list(),
                    "start_time": datetime.datetime.now(),
                },
                "type": "time",
                "id": 'trigger-' + "uuid.uuid4().hex",
                "name": "default"
            },
            "operation_definition": {
                "max_backups": random.randint(1, 99999),
                "retention_duration_days": random.randint(1, 99999),
                "year_backups": random.randint(0, 100),
                "day_backups": random.randint(0, 100),
                "month_backups": random.randint(0, 100),
                "week_backups": random.randint(0, 100),
                "timezone": 'UTC+0' + str(random.randint(0, 9)) + ':00',
            },
            "operation_type": random.choice(['backup', 'replication']),
            "id": 'id-' + uuid.uuid4().hex,
        }

        obj = policy.Policy.existing(**object_info)
        return obj


class FakePolicyFixed(test_base.Fake):
    """Fake one or more CBR policies with fixed associated vaults and
        schedule patterns.
    """

    @classmethod
    def generate(cls):
        object_info = {
            "name": 'name-' + uuid.uuid4().hex,
            "associated_vaults": [
                {'vault_id': 'vault_id_1'},
                {'vault_id': 'vault_id_2'},
                {'vault_id': 'vault_id_3'},
            ],
            "enabled": random.choice([True, False]),
            "trigger": {
                "properties": {
                    "pattern": [
                        'pattern_1',
                        'pattern_2'
                    ],
                    "start_time": datetime.datetime.now(),
                },
                "type": "time",
                "id": 'trigger-' + "uuid.uuid4().hex",
                "name": "default"
            },
            "operation_definition": {
                "max_backups": random.randint(1, 99999),
                "retention_duration_days": random.randint(1, 99999),
                "year_backups": random.randint(0, 100),
                "day_backups": random.randint(0, 100),
                "month_backups": random.randint(0, 100),
                "week_backups": random.randint(0, 100),
                "timezone": 'UTC+0' + str(random.randint(0, 9)) + ':00',
            },
            "operation_type": random.choice(['backup', 'replication']),
            "id": 'id-' + uuid.uuid4().hex,
        }

        obj = policy.Policy.existing(**object_info)
        return obj


class FakeTask(test_base.Fake):
    """Fake one or more CBR task with random vaults list and patterns"""

    @classmethod
    def generate(cls):
        object_info = {
            'status': 'success',
            'provider_id': 'pid-' + uuid.uuid4().hex,
            'checkpoint_id': 'cid-' + uuid.uuid4().hex,
            'updated_at': uuid.uuid4().hex,
            'error_info': {'message': '', 'code': ''},
            'vault_id': 'pid-' + uuid.uuid4().hex,
            'started_at': uuid.uuid4().hex,
            'id': 'id-' + uuid.uuid4().hex,
            'ended_at': uuid.uuid4().hex,
            'created_at': uuid.uuid4().hex,
            'operation_type': 'backup',
            'vault_name': 'vault-' + uuid.uuid4().hex,
            'project_id': 'prjid-' + uuid.uuid4().hex,
            'policy_id': 'polid-' + uuid.uuid4().hex
        }

        obj = task.Task.existing(**object_info)
        return obj


class FakeVault(test_base.Fake):
    """Fake one or more CBR vault with random vaults list and patterns"""

    @classmethod
    def generate(cls):
        object_info = {
            'id': 'id-' + uuid.uuid4().hex,
            'backup_policy_id': 'bid-' + uuid.uuid4().hex,
            'created_at': uuid.uuid4().hex,
            'provider_id': uuid.uuid4().hex,
            'user_id': uuid.uuid4().hex,
            'billing': {
                'cloud_type': 'public',
                'consistent_level': 'crash_consistent',
                'object_type': 'server',
                'protect_type': 'backup',
                'size': random.randint(0, 100),
                'charging_mode': 'post_paid',
                'is_auto_renew': False,
                'is_auto_pay': False,
            },
            'description': 'vault_description',
            'auto_bind': False,
            'name': 'vault-' + uuid.uuid4().hex,
            'resources': [{
                'extra_info': {
                    'include_volumes': [{
                        'id': 'vid-' + uuid.uuid4().hex,
                        'os_version': 'CentOS 7.6 64bit'
                    }]
                },
                'id': 'resource_id',
                'type': 'OS::Nova::Server'
            }],
            'tags': [{
                'key': 'key-tags',
                'value': 'val-tags'
            }],
            'bind_rules': {
                'tags': [{
                    'key': 'key-bind',
                    'value': 'val-bind'
                }]
            },
            'project_id': '0'
        }

        obj = vault.Vault.existing(**object_info)
        return obj


class VaultDefaultStruct:
    def __init__(self, **entries):
        self.__dict__.update(entries)
