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

from otcextensions.osclient.sdrs.v1 import job
from otcextensions.tests.unit.osclient.sdrs.v1 import fakes


class TestJob(fakes.TestSDRS):
    object = fakes.FakeJob.create_one()
    columns = ('id', 'status', 'job_type',
               'begin_time', 'end_time')

    data = [object.job_id,
            object.status,
            object.job_type,
            object.begin_time,
            object.end_time]

    def setUp(self):
        super(TestJob, self).setUp()

        self.cmd = job.ShowJob(self.app, None)
        self.client.get_job = mock.Mock(return_value=self.object)
        self.client.api_mock = self.client.get_job
        if not self.object.error_code:
            self.data, self.columns = job._add_sub_jobs_to_obj(
                self.object,
                self.data,
                self.columns)

        else:
            self.data, self.columns = job._add_parsed_task_to_obj(
                self.object,
                self.data,
                self.columns)

    def test_flatten(self):
        obj = fakes.FakeJob.create_one()

        flat_data = job._flatten_job(obj)

        data = (
            flat_data['id'],
            flat_data['status'],
            flat_data['job_type'],
            flat_data['begin_time'],
            flat_data['end_time']
        )

        cmp_data = (
            obj.job_id,
            obj.status,
            obj.job_type,
            obj.begin_time,
            obj.end_time
        )

        self.assertEqual(data, cmp_data)

    def test_default(self):
        arglist = [
            'job'
        ]

        verifylist = [('job', 'job')]

        # Verify cm is triggered with default parameters
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # Set the response
        self.client.api_mock.side_effect = [
            self.object
        ]

        # Trigger the action
        columns, data = self.cmd.take_action(parsed_args)

        self.client.get_job.assert_called_once_with(job='job')

        self.assertEqual(self.columns, columns)
        self.assertEqual(self.data, list(data))
