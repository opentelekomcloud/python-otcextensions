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
from otcextensions.sdk.ctsv3.v3 import tracker
EXAMPLE = {
    "tracker_type": "system",
    "tracker_name": "system",
    "obs_info": {
        "is_obs_created": False,
        "bucket_name": "test-data-tracker",
        "file_prefix_name": "11"
    },
}


class TestTracker(base.TestCase):
    def test_basic(self):
        sot = tracker.Tracker()
        self.assertEqual('/trackers', sot.base_path)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_delete)

    def test_make_it(self):
        sot = tracker.Tracker(**EXAMPLE)
        self.assertEqual(EXAMPLE['tracker_type'], sot.tracker_type)
        self.assertEqual(EXAMPLE['tracker_name'], sot.tracker_name)
        self.assertEqual(EXAMPLE['obs_info']['is_obs_created'],
                         sot.obs_info.is_obs_created)
        self.assertEqual(EXAMPLE['obs_info']['bucket_name'],
                         sot.obs_info.bucket_name)
        self.assertEqual(EXAMPLE['obs_info']['file_prefix_name'],
                         sot.obs_info.file_prefix_name)
