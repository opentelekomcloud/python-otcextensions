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

import mock

from otcextensions.osclient.mrs.v1 import jobbinary
from otcextensions.tests.unit.osclient.mrs.v1 import fakes


class TestListJobbinary(fakes.TestMrs):
    objects = fakes.FakeJobbinary.create_multiple(3)

    columns = (
        'id', 'name', 'url',
        'description', 'is_public',
        'is_protected'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListJobbinary, self).setUp()

        self.cmd = jobbinary.ListJobbinary(self.app, None)

        self.client.jobs = mock.Mock()
        self.client.api_mock = self.client.jobbinaries

    def test_default(self):
        arglist = [
        ]
        verifylist = [
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
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))


class TestShowJobbinary(fakes.TestMrs):
    object = fakes.FakeJobbinary.create_one()

    columns = (
        'created_at', 'description', 'id',
        'is_protected', 'is_public', 'name',
        'updated_at', 'url'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestShowJobbinary, self).setUp()

        self.cmd = jobbinary.ShowJobbinary(self.app, None)

        self.client.find_jobbinary = mock.Mock()

    def test_default(self):
        arglist = [
            'jobbin'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_jobbinary.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_jobbinary.assert_called_once_with(
            'jobbin',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteJobbinary(fakes.TestMrs):

    def setUp(self):
        super(TestDeleteJobbinary, self).setUp()

        self.cmd = jobbinary.DeleteJobbinary(self.app, None)

        self.client.delete_jobbinary = mock.Mock()

    def test_delete(self):
        arglist = [
            'jobbinary'
        ]
        verifylist = []
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_jobbinary.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                'jobbinary',
                ignore_missing=False),
        ]

        self.client.delete_jobbinary.assert_has_calls(delete_calls)
        self.assertEqual(1, self.client.delete_jobbinary.call_count)


class TestCreateJobbinary(fakes.TestMrs):
    object = fakes.FakeJobbinary.create_one()

    columns = (
        'created_at', 'description', 'id',
        'is_protected', 'is_public', 'name',
        'updated_at', 'url'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestCreateJobbinary, self).setUp()

        self.cmd = jobbinary.CreateJobbinary(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_jobbinary = mock.Mock()

    def test_default(self):
        arglist = [
            '--name', 'test_jb',
            '--url', '/simple/mapreduce/program',
            '--description', 'test',
        ]
        verifylist = [
            ('name', 'test_jb'),
            ('url', '/simple/mapreduce/program'),
            ('description', 'test'),
        ]

        # Verify cmd is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_jobbinary.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_jobbinary.assert_called_once_with(
            name='test_jb',
            url='/simple/mapreduce/program',
            description='test',
            is_public='false'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateJobbinary(fakes.TestMrs):
    object = fakes.FakeJob.create_one()

    columns = (
        'created_at', 'description', 'id',
        'interface', 'is_protected', 'is_public',
        'libs', 'mains', 'name', 'type', 'updated_at'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestUpdateJobbinary, self).setUp()

        self.cmd = jobbinary.UpdateJobbinary(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_jobbinary = mock.Mock()

    def test_default(self):
        arglist = [
            'jobbinary_id',
            '--name', 'test_jb',
        ]
        verifylist = [
            ('jobbinary', 'jobbinary_id'),
            ('name', 'test_jb'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_jobbinary.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_jobbinary.assert_called_with(
            'jobbinary_id',
            ignore_missing=False)

        self.client.update_jobbinary.assert_called_once_with(
            jobbinary=mock.ANY,
            name='test_jb',
            is_public='false'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
