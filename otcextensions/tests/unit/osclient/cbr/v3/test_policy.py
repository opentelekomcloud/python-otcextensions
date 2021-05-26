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
import argparse
import mock

from otcextensions.osclient.cbr.v3 import policy
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestPolicy(fakes.TestCBR):

    def setUp(self):
        super(TestPolicy, self).setUp()

    def test_flatten(self):
        obj = fakes.FakePolicy.create_one()

        flat_data = policy._flatten_policy(obj)

        data = (
            flat_data['id'],
            flat_data['name'],
            flat_data['enabled'],
            flat_data['operation_type'],
            flat_data['retention_duration_days'],
            flat_data['max_backups'],
            flat_data['year_backups'],
            flat_data['day_backups'],
            flat_data['week_backups'],
            flat_data['month_backups'],
            flat_data['timezone'],
            flat_data['start_time']
        )

        od = obj.operation_definition
        cmp_data = (
            obj.id,
            obj.name,
            obj.enabled,
            obj.operation_type,
            od.retention_duration_days,
            od.max_backups,
            od.year_backups,
            od.day_backups,
            od.week_backups,
            od.month_backups,
            od.timezone,
            obj.trigger.properties.start_time,
        )

        self.assertEqual(data, cmp_data)


class TestListPolicy(fakes.TestCBR):

    objects = fakes.FakePolicy.create_multiple(3)

    columns = ('ID', 'name', 'operation_type', 'start_time', 'enabled')

    data = []

    for s in objects:
        flat_data = policy._flatten_policy(s)
        data.append((
            flat_data['id'],
            flat_data['name'],
            flat_data['operation_type'],
            flat_data['start_time'],
            flat_data['enabled']
        ))

    def setUp(self):
        super(TestListPolicy, self).setUp()

        self.cmd = policy.ListPolicies(self.app, None)

        self.client.policies = mock.Mock()
        self.client.api_mock = self.client.policies

    def test_default(self):
        arglist = [
            '--vault-id', 'vault_id',
            '--operation-type', 'backup'
        ]

        verifylist = [
            ('vault_id', 'vault_id'),
            ('operation_type', 'backup')
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with(
            vault_id='vault_id',
            operation_type='backup',
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))

'''
class TestShowPolicy(fakes.TestCBR):

    object = fakes.FakePolicy.create_one()

    columns = (
        'ID',
        'name',
        'operation_type',
        'start_time',
        'enabled',
        'retention_duration_days',
        'max_backups',
        'day_backups',
        'week_backups',
        'month_backups',
        'year_backups',
        'timezone',
    )

    flat_data = policy._flatten_policy(object)

    data = (
        flat_data['id'],
        flat_data['name'],
        flat_data['operation_type'],
        flat_data['start_time'],
        flat_data['enabled'],
        flat_data['retention_duration_days'],
        flat_data['max_backups'],
        flat_data['day_backups'],
        flat_data['week_backups'],
        flat_data['month_backups'],
        flat_data['year_backups'],
        flat_data['timezone'],
    )

    def setUp(self):
        super(TestShowPolicy, self).setUp()

        self.cmd = policy.ShowPolicy(self.app, None)

        self.client.find_policy = mock.Mock()

    def test_default(self):
        arglist = [
            'policy'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_policy.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_policy.assert_called_once_with(
            name_or_id='policy',
            ignore_missing=False,
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
'''
