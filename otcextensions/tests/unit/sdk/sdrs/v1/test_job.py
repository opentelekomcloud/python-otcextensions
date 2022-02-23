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

import uuid
from keystoneauth1 import adapter
import mock
from openstack.tests.unit import base

from otcextensions.sdk.sdrs.v1 import job as _job


EXAMPLE = {
    'job_id': uuid.uuid4()
}


class TestJob(base.TestCase):

    def setUp(self):
        super(TestJob, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)
        self.sess.get = mock.Mock()
        self.sess.default_microversion = '1'
        self.sess._get_connection = mock.Mock(return_value=self.cloud)
        self.sot = _job.Job()

    def test_basic(self):
        sot = _job.Job()
        self.assertEqual('/jobs',
                         sot.base_path)

    def test_make_it(self):
        test_job = _job.Job(**EXAMPLE)
        self.assertEqual(
            EXAMPLE['job_id'],
            test_job.job_id)
