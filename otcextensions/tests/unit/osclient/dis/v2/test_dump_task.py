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
#
import mock
from unittest.mock import call

from osc_lib import exceptions

from otcextensions.osclient.dis.v2 import dump_task
from otcextensions.osclient.dis.v2 import dis_utils
from otcextensions.tests.unit.osclient.dis.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListDumpTasks(fakes.TestDis):

    objects = fakes.FakeDumpTask.create_multiple(3)

    column_list_headers = (
        'Task Name',
        'Task Id',
        'Destination Type',
        'Created At',
        'Status'
    )

    columns = (
        'task_name',
        'task_id',
        'destination_type',
        'created_at',
        'status',
    )

    data = []

    for s in objects:
        data.append((
            s.task_name,
            s.task_id,
            s.destination_type,
            dis_utils.UnixTimestampFormatter(s.created_at),
            s.status
        ))

    def setUp(self):
        super(TestListDumpTasks, self).setUp()

        self.cmd = dump_task.ListDumpTasks(self.app, None)

        self.client.dump_tasks = mock.Mock()
        self.client.api_mock = self.client.dump_tasks

    def test_list(self):
        arglist = [
            'test-stream',
        ]

        verifylist = [
            ('streamName', 'test-stream'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with('test-stream')

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))


class TestCreateDumpTask(fakes.TestDis):
    _data = fakes.FakeDumpTask.create_one()

    columns = (
        'created_at',
        'destination_type',
        'exception_strategy',
        'last_transfer_timestamp',
        'obs_destination_description',
        'partitions',
        'status',
        'stream_name',
        'task_id',
        'task_name'
    )

    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestCreateDumpTask, self).setUp()

        self.cmd = dump_task.CreateDumpTask(self.app, None)
        self.client.create_dump_task = mock.Mock()
        self.client.get_dump_task = mock.Mock(return_value=self._data)

    def test_create(self):
        arglist = [
            'test-stream',
            'test-dump-task',
            '--destination-type', 'OBS',
            '--agency-name', '4',
            '--deliver-time-interval', '5',
            '--consumer-strategy', 'LATEST',
            '--file-prefix', '7',
            '--partition-format', 'yyyy',
            '--obs-bucket-path', '8',
            '--destination-file-type', 'Text',
            '--record-delimiter', '\\n',
        ]
        verifylist = [
            ('streamName', 'test-stream'),
            ('taskName', 'test-dump-task'),
            ('destination_type', 'OBS'),
            ('agency_name', '4'),
            ('deliver_time_interval', 5),
            ('consumer_strategy', 'LATEST'),
            ('file_prefix', '7'),
            ('partition_format', 'yyyy'),
            ('obs_bucket_path', '8'),
            ('destination_file_type', 'Text'),
            ('record_delimiter', '\\n'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        attrs = {}
        attrs.update(
            destination_type='OBS',
            obs_destination_descriptor={
                'task_name': 'test-dump-task',
                'agency_name': '4',
                'deliver_time_interval': 5,
                'consumer_strategy': 'LATEST',
                'file_prefix': '7',
                'partition_format': 'yyyy',
                'obs_bucket_path': '8',
                'destination_file_type': 'Text',
                'record_delimiter': '\\n'
            }
        )

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_dump_task.assert_called_with('test-stream', **attrs)
        self.assertEqual(self.columns, columns)


class TestShowDumpTask(fakes.TestDis):
    _data = fakes.FakeDumpTask.create_one()

    columns = (
        'created_at',
        'destination_type',
        'exception_strategy',
        'last_transfer_timestamp',
        'obs_destination_description',
        'partitions',
        'status',
        'stream_name',
        'task_id',
        'task_name'
    )
    data = fakes.gen_data(_data, columns, dump_task._formatters)

    def setUp(self):
        super(TestShowDumpTask, self).setUp()

        self.cmd = dump_task.ShowDumpTask(self.app, None)

        self.client.get_dump_task = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.stream_name,
            self._data.task_name,
        ]

        verifylist = [
            ('streamName', self._data.stream_name),
            ('taskName', self._data.task_name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_dump_task.assert_called_with(
            self._data.stream_name, self._data.task_name
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            self._data.stream_name,
            'unexist_dis_dump_task',
        ]

        verifylist = [
            ('streamName', self._data.stream_name),
            ('taskName', 'unexist_dis_dump_task'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.get_dump_task = (
            mock.Mock(side_effect=get_mock_result)
        )
        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_dump_task.assert_called_with(
            self._data.stream_name, 'unexist_dis_dump_task')


class TestDeleteDumpTask(fakes.TestDis):

    _data = fakes.FakeDumpTask.create_multiple(2)

    def setUp(self):
        super(TestDeleteDumpTask, self).setUp()

        self.client.delete_dump_task = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = dump_task.DeleteDumpTask(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].stream_name,
            self._data[0].task_name,
        ]

        verifylist = [
            ('streamName', self._data[0].stream_name),
            ('taskName', [self._data[0].task_name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_dump_task.assert_called_with(
            self._data[0].stream_name, self._data[0].task_name)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = [
            self._data[0].stream_name,
            self._data[0].task_name,
            self._data[1].task_name
        ]

        verifylist = [
            ('streamName', self._data[0].stream_name),
            ('taskName', [self._data[0].task_name, self._data[1].task_name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = [
            call(self._data[0].stream_name, self._data[0].task_name),
            call(self._data[0].stream_name, self._data[1].task_name)
        ]
        self.client.delete_dump_task.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].stream_name,
            self._data[0].task_name,
            'unexist_dis_dump_task',
        ]
        verifylist = [
            ('streamName', self._data[0].stream_name),
            ('taskName', [self._data[0].task_name, 'unexist_dis_dump_task']),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        delete_mock_result = [None, exceptions.CommandError]
        self.client.find_gateway = (
            mock.Mock(side_effect=delete_mock_result)
        )
        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual(
                '1 of 2 DIS DumpTask(s) failed to delete.', str(e))

        calls = [
            call(self._data[0].stream_name, self._data[0].task_name),
            call(self._data[0].stream_name, 'unexist_dis_dump_task')
        ]
        self.client.delete_dump_task.assert_has_calls(calls)


class TestStartDumpTask(fakes.TestDis):

    default_timeout = 300

    def setUp(self):
        super(TestStartDumpTask, self).setUp()
        self.cmd = dump_task.StartDumpTask(self.app, None)
        self.client.start_dump_task = mock.Mock(return_value=None)
        # self.client.wait_for_cluster = mock.Mock(return_value=True)

    def test_restart(self):

        arglist = [
            'test-stream',
            'test-dump-taskId',
        ]

        verifylist = [
            ('streamName', 'test-stream'),
            ('taskId', ['test-dump-taskId']),
            # ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.start_dump_task.assert_called_with(
            'test-stream',
            ['test-dump-taskId']
        )
        # self.client.wait_for_cluster.assert_called_with(
        #     self._data.id, self.default_timeout)
        self.assertIsNone(result)


class TestPauseDumpTask(fakes.TestDis):

    default_timeout = 300

    def setUp(self):
        super(TestPauseDumpTask, self).setUp()
        self.cmd = dump_task.PauseDumpTask(self.app, None)
        self.client.pause_dump_task = mock.Mock(return_value=None)
        # self.client.wait_for_action = mock.Mock(return_value=True)

    def test_restart(self):

        arglist = [
            'test-stream',
            'test-dump-taskId',
        ]

        verifylist = [
            ('streamName', 'test-stream'),
            ('taskId', ['test-dump-taskId']),
            # ('wait', True),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.pause_dump_task.assert_called_with(
            'test-stream',
            ['test-dump-taskId']
        )
        # self.client.wait_for_cluster.assert_called_with(
        #     self._data.id, self.default_timeout)
        self.assertIsNone(result)
