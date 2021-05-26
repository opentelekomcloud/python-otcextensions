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
import datetime

import mock

from otcextensions.sdk.cbr.v3 import policy
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
                {'vault_id': '91bbf490549346ae821000df631e5c40'},
                {'vault_id': 'ab762b6e0e9047eab21ecf564561b602'},
                {'vault_id': '1ddcbf2c615949ffbb1ad64a0d3fdd57'},
            ],
            "enabled": random.choice([True, False]),
            "trigger": {
                "properties": {
                    "pattern": [
                        'FREQ=WEEKLY;BYDAY=WE,FR,SU;BYHOUR=10;BYMINUTE=04',
                        'FREQ=WEEKLY;BYDAY=FR,SA;BYHOUR=19;BYMINUTE=44'
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
