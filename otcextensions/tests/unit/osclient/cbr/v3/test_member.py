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

from otcextensions.osclient.cbr.v3 import member
from otcextensions.sdk.cbr.v3 import member as memberSDK
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestMember(fakes.TestCBR):

    def setUp(self):
        super(TestMember, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeMember.create_one()

        flat_data = member._flatten_policy(obj)

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
