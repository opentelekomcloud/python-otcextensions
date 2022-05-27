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

from otcextensions.osclient.cbr.v3 import task
from otcextensions.tests.unit.osclient.cbr.v3 import fakes


class TestTask(fakes.TestCBR):

    def setUp(self):
        super(TestTask, self).setUp()

    def test_flatten(self):
        obj = fakes.FakeTask.create_one()

        flat_data = task._flatten_task(obj)

        data = (
            flat_data['id'],
            flat_data['checkpoint_id'],
            flat_data['policy_id'],
            flat_data['provider_id'],
            flat_data['vault_id'],
            flat_data['vault_name'],
            flat_data['operation_type'],
            flat_data['error_mesage'],
            flat_data['error_code'],
            flat_data['created_at'],
            flat_data['ended_at'],
            flat_data['started_at'],
            flat_data['updated_at']
        )

        cmp_data = (
            obj.id,
            obj.checkpoint_id,
            obj.policy_id,
            obj.provider_id,
            obj.vault_id,
            obj.vault_name,
            obj.operation_type,
            obj.error_info.message,
            obj.error_info.code,
            obj.created_at,
            obj.ended_at,
            obj.started_at,
            obj.updated_at,
        )

        self.assertEqual(data, cmp_data)


class TestListTask(fakes.TestCBR):

    objects = fakes.FakeTask.create_multiple(3)

    columns = ('id', 'checkpoint_id', 'provider_id',
               'operation_type', 'created_at', 'ended_at')

    data = []

    for s in objects:
        flat_data = task._flatten_task(s)
        data.append((
            flat_data['id'],
            flat_data['checkpoint_id'],
            flat_data['provider_id'],
            flat_data['operation_type'],
            flat_data['created_at'],
            flat_data['ended_at']
        ))

    def setUp(self):
        super(TestListTask, self).setUp()

        self.cmd = task.ListTasks(self.app, None)

        self.client.tasks = mock.Mock()
        self.client.api_mock = self.client.tasks

    def test_default(self):
        arglist = []

        verifylist = []

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.objects
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_once_with()

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowTask(fakes.TestCBR):

    object = fakes.FakeTask.create_one()

    columns = (
        'id',
        'checkpoint_id',
        'policy_id',
        'provider_id',
        'vault_id',
        'vault_name',
        'operation_type',
        'error_mesage',
        'error_code',
        'created_at',
        'ended_at',
        'started_at',
        'updated_at'
    )

    flat_data = task._flatten_task(object)

    data = (
        flat_data['id'],
        flat_data['checkpoint_id'],
        flat_data['policy_id'],
        flat_data['provider_id'],
        flat_data['vault_id'],
        flat_data['vault_name'],
        flat_data['operation_type'],
        flat_data['error_mesage'],
        flat_data['error_code'],
        flat_data['created_at'],
        flat_data['ended_at'],
        flat_data['started_at'],
        flat_data['updated_at']
    )

    def setUp(self):
        super(TestShowTask, self).setUp()

        self.cmd = task.ShowTask(self.app, None)

        self.client.get_task = mock.Mock()

    def test_default(self):
        arglist = [
            'task'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.get_task.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_task.assert_called_once_with('task')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
