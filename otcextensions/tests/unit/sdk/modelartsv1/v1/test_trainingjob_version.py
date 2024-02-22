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
import copy
from unittest.mock import MagicMock

from openstack.tests.unit import base
from otcextensions.sdk.modelartsv1.v1 import trainingjob_version
from otcextensions.tests.unit.sdk.modelartsv1.v1.examples import \
    EXAMPLE_TRAINING_JOB_VERSION as EXAMPLE


class TestTrainingJobVersion(base.TestCase):
    def setUp(self):
        super(TestTrainingJobVersion, self).setUp()

    def test_basic(self):
        sot = trainingjob_version.TrainingJobVersion()

        self.assertEqual("/training-jobs/%(jobId)s/versions", sot.base_path)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("versions", sot.resources_key)

        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        EXAMPLE2 = copy.deepcopy(EXAMPLE)
        updated_sot_attrs = ["create_time"]
        sot = trainingjob_version.TrainingJobVersion()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = EXAMPLE2
        sot._translate_response(mock_response)
        self.assertEqual(EXAMPLE["create_time"], sot.created_at)
        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)
