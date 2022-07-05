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

from otcextensions.osclient.mrs.v1 import job
from otcextensions.tests.unit.osclient.mrs.v1 import fakes


class TestListJob(fakes.TestMrs):
    objects = fakes.FakeCluster.create_multiple(3)

    columns = (
        'id', 'name', 'type', 'description',
        'is_public', 'is_protected'
    )

    data = []

    for s in objects:
        data.append(fakes.gen_data(s, columns))

    def setUp(self):
        super(TestListJob, self).setUp()

        self.cmd = job.ListJob(self.app, None)

        self.client.jobs = mock.Mock()
        self.client.api_mock = self.client.jobs

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


class TestShowJob(fakes.TestMrs):
    object = fakes.FakeJob.create_one()

    columns = (
        'created_at', 'description', 'id',
        'interface', 'is_protected', 'is_public',
        'libs', 'mains', 'name', 'type', 'updated_at'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestShowJob, self).setUp()

        self.cmd = job.ShowJob(self.app, None)

        self.client.find_job = mock.Mock()

    def test_default(self):
        arglist = [
            'job'
        ]
        verifylist = [
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.find_job.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_job.assert_called_once_with(
            'job',
            ignore_missing=False
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestDeleteJob(fakes.TestMrs):

    def setUp(self):
        super(TestDeleteJob, self).setUp()

        self.cmd = job.DeleteJob(self.app, None)

        self.client.delete_job = mock.Mock()

    def test_delete(self):
        arglist = [
            'job'
        ]
        verifylist = []
        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.delete_job.side_effect = [{}]

        # Trigger the action
        self.cmd.take_action(parsed_args)

        delete_calls = [
            mock.call(
                'job',
                ignore_missing=False),
        ]

        self.client.delete_job.assert_has_calls(delete_calls)
        self.assertEqual(1, self.client.delete_job.call_count)


class TestCreateJob(fakes.TestMrs):
    object = fakes.FakeJob.create_one()

    columns = (
        'created_at', 'description', 'id',
        'interface', 'is_protected', 'is_public',
        'libs', 'mains', 'name', 'type', 'updated_at'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestCreateJob, self).setUp()

        self.cmd = job.CreateJob(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.create_job = mock.Mock()

    def test_default(self):
        arglist = [
            'test_job',
            '--type', 'MapReduce',
            '--description', 'test',
        ]
        verifylist = [
            ('name', 'test_job'),
            ('type', 'MapReduce'),
            ('description', 'test'),
        ]

        # Verify cmd is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.create_job.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.create_job.assert_called_once_with(
            type='MapReduce',
            name='test_job',
            description='test',
            is_public='false',
            is_protected='false'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)


class TestUpdateJob(fakes.TestMrs):
    object = fakes.FakeJob.create_one()

    columns = (
        'created_at', 'description', 'id',
        'interface', 'is_protected', 'is_public',
        'libs', 'mains', 'name', 'type', 'updated_at'
    )

    data = fakes.gen_data(object, columns)

    def setUp(self):
        super(TestUpdateJob, self).setUp()

        self.cmd = job.UpdateJob(self.app, None)
        self.app.client_manager.sdk_connection = mock.Mock()

        self.client.update_datasource = mock.Mock()

    def test_default(self):
        arglist = [
            'job_id',
            '--name', 'test_job',
            '--type', 'Hive',
            '--description', 'updated',
        ]
        verifylist = [
            ('job', 'job_id'),
            ('name', 'test_job'),
            ('type', 'Hive'),
            ('description', 'updated'),
        ]

        # Verify cm is triggereg with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.update_job.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.find_job.assert_called_with(
            'job_id',
            ignore_missing=False)

        self.client.update_job.assert_called_once_with(
            job=mock.ANY,
            name='test_job',
            type='Hive',
            description='updated',
            is_public='false'
        )

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, data)
