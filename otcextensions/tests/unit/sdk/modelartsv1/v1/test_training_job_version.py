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
from openstack.tests.unit import base
from otcextensions.sdk.modelartsv1.v1 import training_job_version
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = examples.TRAINING_JOB_VERSION


class TestTrainingJobVersion(base.TestCase):
    def setUp(self):
        super(TestTrainingJobVersion, self).setUp()

    def test_basic(self):
        sot = training_job_version.TrainingJobVersion()

        self.assertEqual("/training-jobs/%(jobId)s/versions", sot.base_path)
        self.assertEqual("versions", sot.resources_key)
        self.assertEqual(None, sot.resource_key)

        self.assertTrue(sot.allow_fetch)
        self.assertTrue(sot.allow_list)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertFalse(sot.allow_commit)

    def test_make_it(self):
        sot = training_job_version.TrainingJobVersion(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key == "create_time":
                self.assertEqual(EXAMPLE["create_time"], sot.created_at)
            elif key == "start_time":
                self.assertEqual(EXAMPLE["start_time"], sot.started_at)
            elif key == "system_metric_list":
                updated_sot_attrs = {
                    "cpuUsage": "cpu_usage",
                    "memUsage": "mem_usage",
                    "gpuUtil": "gpu_util",
                    "gpuMemUsage": "gpu_mem_usage",
                    "diskReadRate": "disk_read_rate",
                    "diskWriteRate": "disk_write_rate",
                    "recvBytesRate": "recv_bytes_rate",
                    "sendBytesRate": "send_bytes_rate",
                }

                for k1, v1 in updated_sot_attrs.items():
                    self.assertEqual(
                        getattr(sot.system_metric_list, v1),
                        EXAMPLE["system_metric_list"][k1],
                    )
            else:
                assert_attributes_equal(self, getattr(sot, key), value)
