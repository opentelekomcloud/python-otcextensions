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
import mock

from otcextensions.osclient.cbr.v3 import policy
from otcextensions.sdk.cbr.v3 import policy as policySDK
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

    def test_add_vaults_to_policy_output(self):
        obj = fakes.FakePolicyFixed.create_one()

        column = ()
        data = ()
        verify_column = (
            'associated_vault_1',
            'associated_vault_2',
            'associated_vault_3',
        )
        verify_data = (
            'vault_id_1',
            'vault_id_2',
            'vault_id_3',
        )

        data, column = policy._add_vaults_to_policy_obj(obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)

    def test_add_scheduling_patterns(self):
        obj = fakes.FakePolicyFixed.create_one()

        column = ()
        data = ()
        verify_column = (
            'schedule_pattern_1',
            'schedule_pattern_2'
        )
        verify_data = (
            'pattern_1',
            'pattern_2'
        )

        data, column = policy._add_scheduling_patterns(obj, data, column)

        self.assertEqual(data, verify_data)
        self.assertEqual(column, verify_column)


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
            policy_id='policy',
            ignore_missing=False,
        )

        self.data, self.columns = policy._add_vaults_to_policy_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = policy._add_scheduling_patterns(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeletePolicy(fakes.TestCBR):

    def setUp(self):
        super(TestDeletePolicy, self).setUp()

        self.cmd = policy.DeletePolicy(self.app, None)

        self.client.delete_policy = mock.Mock()

    def test_delete(self):
        arglist = [
            'p1'
        ]
        verifylist = [
            ('policy', 'p1')
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_policy.side_effect = [{}]

        # Set the response for find_policy
        self.client.find_policy.side_effect = [
            policySDK.Policy(id='p1')
        ]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                policy='p1',
                ignore_missing=False),
        ]

        find_calls = [
            mock.call(
                name_or_id='p1',
                ignore_missing=False),
        ]

        self.client.delete_policy.assert_has_calls(delete_calls)
        self.client.find_policy.assert_has_calls(find_calls)
        self.assertEqual(1, self.client.delete_policy.call_count)


class TestCreatePolicy(fakes.TestCBR):

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
        super(TestCreatePolicy, self).setUp()

        self.cmd = policy.CreatePolicy(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_policy = mock.Mock()

    def test_default(self):
        arglist = [
            'policy_name',
            '--disable',
            '--operation-type', 'backup',
            '--pattern', 'pattern_1',
            '--pattern', 'pattern_2',
            '--day-backups', '1',
            '--week-backups', '2',
            '--month-backups', '3',
            '--year-backups', '4',
            '--timezone', 'tz',
            '--max-backups', '10',
            '--retention-duration-days', '9'
        ]
        verifylist = [
            ('name', 'policy_name'),
            ('disable', False),
            ('operation_type', 'backup'),
            ('patterns', ['pattern_1', 'pattern_2']),
            ('day_backups', 1),
            ('week_backups', 2),
            ('month_backups', 3),
            ('year_backups', 4),
            ('timezone', 'tz'),
            ('max_backups', 10),
            ('retention_duration_days', 9),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_policy.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_policy.assert_called_once_with(
            operation_definition={
                'day_backups': 1,
                'week_backups': 2,
                'month_backups': 3,
                'year_backups': 4,
                'max_backups': 10,
                'retention_duration_days': 9,
                'timezone': 'tz'},
            trigger={
                'properties': {
                    'pattern': ['pattern_1', 'pattern_2']}},
            name='policy_name',
            enabled=False,
            operation_type='backup'
        )

        self.data, self.columns = policy._add_scheduling_patterns(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdatePolicy(fakes.TestCBR):

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
        super(TestUpdatePolicy, self).setUp()

        self.cmd = policy.UpdatePolicy(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_policy = mock.Mock()

    def test_default(self):
        arglist = [
            'policy_id',
            '--name', 'pol1',
            '--enable',
            '--pattern', 'pattern_1',
            '--pattern', 'pattern_2',
            '--day-backups', '1',
            '--week-backups', '2',
            '--month-backups', '3',
            '--year-backups', '4',
            '--timezone', 'tz',
            '--max-backups', '10',
            '--retention-duration-days', '9'
        ]
        verifylist = [
            ('policy', 'policy_id'),
            ('name', 'pol1'),
            ('enable', True),
            ('patterns', ['pattern_1', 'pattern_2']),
            ('day_backups', 1),
            ('week_backups', 2),
            ('month_backups', 3),
            ('year_backups', 4),
            ('timezone', 'tz'),
            ('max_backups', 10),
            ('retention_duration_days', 9),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_policy.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_policy.assert_called_with(
            policy_id='policy_id',
            ignore_missing=False)

        self.client.update_policy.assert_called_once_with(
            policy=mock.ANY,
            name='pol1',
            enabled=True,
            trigger={
                'properties': {
                    'pattern': ['pattern_1', 'pattern_2']}},
            operation_definition={
                'day_backups': 1,
                'week_backups': 2,
                'month_backups': 3,
                'year_backups': 4,
                'max_backups': 10,
                'retention_duration_days': 9,
                'timezone': 'tz'}
        )

        self.data, self.columns = policy._add_vaults_to_policy_obj(
            self.object,
            self.data,
            self.columns
        )

        self.data, self.columns = policy._add_scheduling_patterns(
            self.object,
            self.data,
            self.columns
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
