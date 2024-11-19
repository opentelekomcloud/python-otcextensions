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
import openstack
from otcextensions.tests.functional.sdk.ctsv3 import TestCtsv3

_logger = openstack._log.setup_logging('openstack')


class TestTracker(TestCtsv3):
    uuid_v4 = uuid.uuid4().hex[:8]
    bucket_name = 'obs-test-' + uuid_v4
    container = None

    def setUp(self):
        super(TestTracker, self).setUp()
        self.client_obs = self.conn.obs
        self.container = self.client_obs.create_container(
            name=self.bucket_name,
            storage_acl='public-read',
        )
        self.cts = self.conn.ctsv3
        attrs = {
            "tracker_type": "system",
            "tracker_name": "system",
            "obs_info": {
                "is_obs_created": False,
                "bucket_name": self.bucket_name,
                "file_prefix_name": "test-prefix"
            },
            "status": "enabled",
            "is_lts_enabled": True,
        }
        self.tracker = self.cts.create_tracker(**attrs)

    def tearDown(self):
        super(TestTracker, self).tearDown()
        try:
            if self.tracker:
                self.client.delete_tracker(self.tracker)
        except openstack.exceptions.SDKException as e:
            _logger.warning('Got exception during clearing resources %s'
                            % e.message)
        objects = self.client_obs.objects(
            container=self.container
        )
        for obj in objects:
            self.client_obs.delete_object(obj, container=self.container)
        self.addCleanup(self.client_obs.delete_container, self.container)


    def test_01_list_trackers(self):
        trackers = list(self.conn.ctsv3.trackers())
        self.assertIsNotNone(trackers)

    def test_02_update_tracker(self):
        attrs = {
            "tracker_type": "system",
            "tracker_name": "system",
            "obs_info": {
                "is_obs_created": False,
                "bucket_name": self.bucket_name,
                "file_prefix_name": "test-prefix"
            },
            "status": "disabled",
            "is_lts_enabled": False,
            "is_support_trace_files_encryption": True,
            "kms_id": "",
            "is_support_validate": False,
        }
        self.conn.ctsv3.update_tracker(**attrs)
        attrs = {
            "tracker_name": "system"
        }
        tracker = list(self.conn.ctsv3.trackers(**attrs))[0]
        self.assertEqual(tracker.status, "disabled")
