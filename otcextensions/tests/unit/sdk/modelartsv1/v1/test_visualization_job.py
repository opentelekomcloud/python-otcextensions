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
from keystoneauth1 import adapter

from openstack.tests.unit import base
from otcextensions.sdk.modelartsv1.v1 import visualization_job

EXAMPLE = {
    "duration": 33000,
    "service_url": "https://...",
    "job_name": "apiTest-11",
    "create_time": 1565149736000,
    "train_url": "/wph-test/zl-test/Flowers-Set/ApiTest/",
    "job_id": 197,
    "job_desc": "ModelArts API Dialtest",
    "resource_id": "e17dd874-b5e0-4e9b-aaf0-22b045ad8571",
    "remaining_duration": None,
    "is_success": True,
    "status": 7,
}


class TestVisualizationJob(base.TestCase):
    def setUp(self):
        super(TestVisualizationJob, self).setUp()
        self.sess = mock.Mock(spec=adapter.Adapter)

    def test_basic(self):
        sot = visualization_job.VisualizationJob()

        self.assertEqual("/visualization-jobs", sot.base_path)
        self.assertEqual("jobs", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_commit)

    def test_make_it(self):
        sot = visualization_job.VisualizationJob(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key == "create_time":
                self.assertEqual(EXAMPLE["create_time"], sot.created_at)
            else:
                self.assertEqual(getattr(sot, key), value)

    def test_action(self):
        data = {"id": "mock-id"}
        sot = visualization_job.VisualizationJob(**data)
        action = "restart"
        response = mock.Mock()
        response.status_code = 200
        response.json.return_value = data
        response.headers = {}
        self.sess.post.return_value = response
        rt = sot._action(self.sess, action)
        self.sess.post.assert_called_with(
            f"visualization-jobs/{sot.id}/{action}",
            json=None,
        )
        self.assertEqual(rt, sot)

    def test_restart(self):
        sot = visualization_job.VisualizationJob.existing(id=EXAMPLE["job_id"])
        sot._action = mock.Mock()
        sot.restart(self.sess)
        sot._action.assert_called_with(self.sess, "restart")

    def test_stop(self):
        sot = visualization_job.VisualizationJob.existing(id=EXAMPLE["job_id"])
        sot._action = mock.Mock()
        sot.stop(self.sess)
        sot._action.assert_called_with(self.sess, "stop")
