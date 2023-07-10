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

from otcextensions.osclient.dis.v2 import stream
from otcextensions.sdk.dis.v2 import stream as sdk_stream
from otcextensions.tests.unit.osclient.dis.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestListStreams(fakes.TestDis):

    objects = fakes.FakeStream.create_multiple(3)

    column_list_headers = (
        'Name',
        'Stream Type',
        'Data Type',
        'Partition Count',
        'AutoScale Enabled',
        'Status'
    )

    columns = (
        'name',
        'stream_type',
        'data_type',
        'partition_count',
        'is_auto_scale_enabled',
        'status'
    )

    data = []

    for s in objects:
        data.append((
            s.name,
            s.stream_type,
            s.data_type,
            s.partition_count,
            s.is_auto_scale_enabled,
            s.status
        ))

    def setUp(self):
        super(TestListStreams, self).setUp()

        self.cmd = stream.ListStreams(self.app, None)

        self.client.streams = mock.Mock()
        self.client.api_mock = self.client.streams

    def test_list(self):
        arglist = []

        verifylist = []

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with()

        self.assertEqual(self.column_list_headers, columns)
        self.assertEqual(self.data, list(data))

    def test_list_args(self):
        arglist = [
            '--limit', '1',
            '--start-stream-name', '2',
        ]

        verifylist = [
            ('limit', 1),
            ('start_stream_name', '2'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [self.objects]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.api_mock.assert_called_with(
            limit=1,
            start_stream_name='2',
        )


class TestCreateStream(fakes.TestDis):

    columns = (
        'auto_scale_max_partition_count',
        'auto_scale_min_partition_count',
        'compression_format',
        'data_duration',
        'data_type',
        'is_auto_scale_enabled',
        'name',
        'partition_count',
        'stream_type',
        'sys_tags',
        'tags'
    )

    def setUp(self):
        super(TestCreateStream, self).setUp()

        self.cmd = stream.CreateStream(self.app, None)

    def test_create(self):
        arglist = [
            'test-stream',
            '--partition-count', '2',
            '--stream-type', '3',
            '--data-type', '4',
            '--data-duration', '5',
            '--autoscale-min-count', '6',
            '--autoscale-max-count', '7',
            '--compression-format', '8',
            '--tag', 'key=k1,value=v1',
            '--tag', 'key=k2,value=v2',
            '--sys-tag', 'key=sysk1,value=sysv1',
            '--sys-tag', 'key=sysk2,value=sysv2',
            '--autoscale',
        ]
        verifylist = [
            ('name', 'test-stream'),
            ('partition_count', 2),
            ('stream_type', '3'),
            ('data_type', '4'),
            ('data_duration', 5),
            ('auto_scale_min_partition_count', 6),
            ('auto_scale_max_partition_count', 7),
            ('compression_format', '8'),
            ('tags', [{'key': 'k1', 'value': 'v1'},
                      {'key': 'k2', 'value': 'v2'}]),
            ('sys_tags', [{'key': 'sysk1', 'value': 'sysv1'},
                          {'key': 'sysk2', 'value': 'sysv2'}]),
            ('autoscale', True),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        attrs = {}
        attrs.update(
            name='test-stream',
            partition_count=2,
            stream_type='3',
            data_type='4',
            data_duration=5,
            auto_scale_min_partition_count=6,
            auto_scale_max_partition_count=7,
            compression_format='8',
            tags=[{'key': 'k1', 'value': 'v1'}, {'key': 'k2', 'value': 'v2'}],
            sys_tags=[{'key': 'sysk1', 'value': 'sysv1'},
                      {'key': 'sysk2', 'value': 'sysv2'}],
            auto_scale_enabled=True
        )

        self.client.create_stream = mock.Mock(
            return_value=sdk_stream.Stream(**attrs))

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_stream.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestUpdateStreamPartition(fakes.TestDis):

    stream_name = 'test-dis-stream'

    _data = sdk_stream.Stream(
        stream_name=stream_name,
        current_partition_count=4,
        target_partition_count=2
    )

    display_columns = (
        'stream_name',
        'current_partition_count',
        'target_partition_count',
    )

    columns = (
        'name',
        'current_partition_count',
        'target_partition_count',
    )

    data = fakes.gen_data(_data, columns, stream._formatters)

    def setUp(self):
        super(TestUpdateStreamPartition, self).setUp()

        self.cmd = stream.UpdateStreamPartition(self.app, None)

        self.client.update_stream_partition = \
            mock.Mock(return_value=self._data)

    def test_update(self):
        arglist = [
            self._data.name,
            '--partition-count', '2',
        ]
        verifylist = [
            ('stream', self._data.name),
            ('partition_count', 2),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.update_stream_partition.assert_called_with(
            'test-dis-stream',
            stream_name='test-dis-stream',
            target_partition_count=2
        )
        self.assertEqual(self.display_columns, columns)


class TestShowStream(fakes.TestDis):

    _data = fakes.FakeStream.create_one()
    columns = (
        'auto_scale_max_partition_count',
        'auto_scale_min_partition_count',
        'compression_format',
        'created_at',
        'data_type',
        'has_more_partitions',
        'id',
        'is_auto_scale_enabled',
        'name',
        'partitions',
        'readable_partition_count',
        'retention_period',
        'status',
        'stream_type',
        'updated_at',
        'writable_partition_count'
    )

    data = fakes.gen_data(_data, columns, stream._formatters)

    def setUp(self):
        super(TestShowStream, self).setUp()

        self.cmd = stream.ShowStream(self.app, None)

        self.client.get_stream = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            self._data.name,
        ]

        verifylist = [
            ('stream', self._data.name),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_stream.assert_called_with(self._data.name)

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)

    def test_show_non_existent(self):
        arglist = [
            'unexist_dis_stream',
        ]

        verifylist = [
            ('stream', 'unexist_dis_stream'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        get_mock_result = exceptions.CommandError('Resource Not Found')
        self.client.find_stream = (
            mock.Mock(side_effect=get_mock_result)
        )

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('Resource Not Found', str(e))
        self.client.get_stream.assert_called_with('unexist_dis_stream')


class TestDeleteStream(fakes.TestDis):

    _data = fakes.FakeStream.create_multiple(2)

    def setUp(self):
        super(TestDeleteStream, self).setUp()

        self.client.delete_stream = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = stream.DeleteStream(self.app, None)

    def test_delete(self):
        arglist = [
            self._data[0].name,
        ]

        verifylist = [
            ('stream', [self._data[0].name]),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_stream.assert_called_with(self._data[0].name)
        self.assertIsNone(result)

    def test_multiple_delete(self):
        arglist = []

        for dis_stream in self._data:
            arglist.append(dis_stream.name)

        verifylist = [
            ('stream', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)

        calls = []
        for dis_stream in self._data:
            calls.append(call(dis_stream.name))
        self.client.delete_stream.assert_has_calls(calls)
        self.assertIsNone(result)

    def test_multiple_delete_with_exception(self):
        arglist = [
            self._data[0].name,
            'unexist_dis_stream',
        ]
        verifylist = [
            ('stream', arglist),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # delete_mock_result = [None, exceptions.CommandError]

        # Trigger the action
        try:
            self.cmd.take_action(parsed_args)
        except Exception as e:
            self.assertEqual('1 of 2 DIS Stream(s) failed to delete.', str(e))

        calls = [call(self._data[0].name), call('unexist_dis_stream')]
        self.client.delete_stream.assert_has_calls(calls)
