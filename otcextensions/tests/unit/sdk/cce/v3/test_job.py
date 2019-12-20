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
from keystoneauth1 import adapter

import mock

from openstack.tests.unit import base

from otcextensions.sdk.cce.v3 import job as _job


EXAMPLE = {
    "kind": "Job",
    "apiVersion": "v3",
    "metadata": {
        "uid": "397eb2b9-261a-11e9-bcf7-0255ac110e1e",
        "creationTimestamp": "2019-02-01 12:09:28.712099 +0000 UTC",
        "updateTimestamp": "2019-02-01 12:10:20.649724 +0000 UTC"
    },
    "spec": {
    },
    "status": {
        "phase": "Success"
    }
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
        self.assertIsNone(sot.resource_key)
        self.assertIsNone(sot.resources_key)
        self.assertEqual('/jobs',
                         sot.base_path)
        self.assertFalse(sot.allow_list)
        self.assertFalse(sot.allow_create)
        self.assertTrue(sot.allow_fetch)
        self.assertFalse(sot.allow_commit)
        self.assertFalse(sot.allow_delete)

    def test_make_it(self):
        obj = EXAMPLE
        sot = _job.Job.existing(**obj)
        self.assertEqual(obj['metadata']['uid'], sot.id)
        self.assertEqual(obj['kind'], sot.kind)

    def test_get_status(self):
        data = EXAMPLE
        job = _job.Job(**EXAMPLE)

        self.assertEqual(data['status']['phase'], getattr(job,
                                                          'status.status'))
