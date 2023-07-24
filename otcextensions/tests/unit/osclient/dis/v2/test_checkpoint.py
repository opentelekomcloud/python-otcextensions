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

from otcextensions.osclient.dis.v2 import checkpoint
from otcextensions.sdk.dis.v2 import checkpoint as sdk_checkpoint
from otcextensions.tests.unit.osclient.dis.v2 import fakes

from openstackclient.tests.unit import utils as tests_utils


class TestCreateCheckpoint(fakes.TestDis):

    columns = (
        'app_name',
        'checkpoint_type',
        'partition_id',
        'sequence_number',
        'stream_name',
    )

    def setUp(self):
        super(TestCreateCheckpoint, self).setUp()

        self.cmd = checkpoint.CreateCheckpoint(self.app, None)

    def test_create(self):
        arglist = [
            'test-stream',
            'test-app',
            '--partition-id', '1',
            '--sequence-number', '1',
            '--checkpoint-type', 'LAST_READ',
        ]
        verifylist = [
            ('streamName', 'test-stream'),
            ('appName', 'test-app'),
            ('partition_id', '1'),
            ('sequence_number', '1'),
            ('checkpoint_type', 'LAST_READ'),
        ]
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        attrs = {
            'stream_name': 'test-stream',
            'app_name': 'test-app',
            'partition_id': '1',
            'sequence_number': '1',
            'checkpoint_type': 'LAST_READ'
        }

        self.client.create_checkpoint = mock.Mock(
            return_value=sdk_checkpoint.Checkpoint(**attrs))

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_checkpoint.assert_called_with(**attrs)
        self.assertEqual(self.columns, columns)


class TestShowCheckpoint(fakes.TestDis):
    _data = fakes.FakeCheckpoint.create_one()

    columns = ('metadata', 'sequence_number')
    data = fakes.gen_data(_data, columns)

    def setUp(self):
        super(TestShowCheckpoint, self).setUp()

        self.cmd = checkpoint.ShowCheckpoint(self.app, None)

        self.client.get_checkpoint = mock.Mock(return_value=self._data)

    def test_show_no_options(self):
        arglist = []
        verifylist = []

        # Testing that a call without the required argument will fail and
        # throw a "ParserExecption"
        self.assertRaises(tests_utils.ParserException,
                          self.check_parser, self.cmd, arglist, verifylist)

    def test_show(self):
        arglist = [
            'test-stream',
            'test-app',
            '--partition-id', '1',
            '--checkpoint-type', 'LAST_READ',
        ]

        verifylist = [
            ('streamName', 'test-stream'),
            ('appName', 'test-app'),
            ('partition_id', '1'),
            ('checkpoint_type', 'LAST_READ'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)
        self.client.get_checkpoint.assert_called_with(
            stream_name='test-stream',
            app_name='test-app',
            partition_id='1',
            checkpoint_type='LAST_READ'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteCheckpoint(fakes.TestDis):

    _data = fakes.FakeCheckpoint.create_multiple(2)

    def setUp(self):
        super(TestDeleteCheckpoint, self).setUp()

        self.client.delete_checkpoint = mock.Mock(return_value=None)

        # Get the command object to test
        self.cmd = checkpoint.DeleteCheckpoint(self.app, None)

    def test_delete(self):
        arglist = [
            'test-stream',
            'test-app',
            '--partition-id', '1',
            '--checkpoint-type', 'LAST_READ',
        ]

        verifylist = [
            ('streamName', 'test-stream'),
            ('appName', 'test-app'),
            ('partition_id', '1'),
            ('checkpoint_type', 'LAST_READ'),
        ]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Trigger the action
        result = self.cmd.take_action(parsed_args)
        self.client.delete_checkpoint.assert_called_with(
            stream_name='test-stream',
            app_name='test-app',
            partition_id='1',
            checkpoint_type='LAST_READ'
        )

        self.assertIsNone(result)
