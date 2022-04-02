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

from otcextensions.osclient.sdrs.v1 import job
from otcextensions.tests.unit.osclient.sdrs.v1 import fakes


class TestJob(fakes.TestSDRS):

    def setUp(self):
        super(TestJob, self).setUp()

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
