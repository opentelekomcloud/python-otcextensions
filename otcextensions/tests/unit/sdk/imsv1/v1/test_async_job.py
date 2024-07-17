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

from openstack.tests.unit import base

from otcextensions.sdk.imsv1.v1 import async_job

EXAMPLE = {
    "status": "SUCCESS",
    "job_id": "ff8080814dbd65d7014dbe0d84db0013",
    "job_type": "createImageByInstance",
    "begin_time": "04-Jun-2015 18:11:06:586",
    "end_time": "",
    "error_code": "404",
    "fail_reason": "something bad happened"
}


class TestAsyncJob(base.TestCase):

    def test_basic(self):
        sot = async_job.AsyncJob()
        path = ''
        self.assertEqual(path, sot.base_path)
        self.assertTrue(sot.allow_fetch)

    def test_make_it(self):
        sot = async_job.AsyncJob(**EXAMPLE)
        self.assertEqual(EXAMPLE['status'], sot.status)
        self.assertEqual(EXAMPLE['job_id'], sot.job_id)
        self.assertEqual(EXAMPLE['job_type'], sot.job_type)
        self.assertEqual(EXAMPLE['begin_time'], sot.begin_time)
        self.assertEqual(EXAMPLE['end_time'], sot.end_time)
        self.assertEqual(EXAMPLE['error_code'], sot.error_code)
        self.assertEqual(EXAMPLE['fail_reason'], sot.fail_reason)
