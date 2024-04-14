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
from otcextensions.sdk.modelartsv1.v1 import training_job
from otcextensions.tests.unit.sdk.modelartsv1.v1 import examples
from otcextensions.tests.unit.sdk.utils import assert_attributes_equal

EXAMPLE = examples.TRAINING_JOB

EXAMPLE_CREATE = {
    "job_name": "TestModelArtsJob3",
    "workspace_id": "0",
    "config": {
        "worker_server_num": 1,
        "app_url": "/usr/app/",
        "boot_file_url": "/usr/app/boot.py",
        "parameter": [
            {"label": "learning_rate", "value": "0.01"},
            {"label": "batch_size", "value": "32"},
        ],
        "dataset_id": "dataset-id",
        "dataset_version_id": "version-id",
        "spec_id": 1,
        "engine_id": 1,
        "train_url": "/usr/train/",
        "log_url": "/usr/log/",
        "volumes": [
            {
                "nfs": {
                    "id": "nfs-id",
                    "src_path": "192.168.8.150:/",
                    "dest_path": "/home/work/nas",
                    "read_only": False,
                }
            },
            {
                "host_path": {
                    "src_path": "/root/work",
                    "dest_path": "/home/mind",
                    "read_only": False,
                }
            },
        ],
    },
}


class TestTrainingjob(base.TestCase):
    def setUp(self):
        super(TestTrainingjob, self).setUp()

    def test_basic(self):
        sot = training_job.TrainingJob()

        self.assertEqual("/training-jobs", sot.base_path)
        self.assertEqual(None, sot.resource_key)
        self.assertEqual("jobs", sot.resources_key)

        self.assertTrue(sot.allow_commit)
        self.assertTrue(sot.allow_create)
        self.assertTrue(sot.allow_delete)
        self.assertTrue(sot.allow_list)
        self.assertFalse(sot.allow_fetch)

    def test_make_it(self):
        sot = training_job.TrainingJob(**EXAMPLE)
        self.assertEqual(sot.id, EXAMPLE["job_id"])
        for key, value in EXAMPLE.items():
            if key == "create_time":
                self.assertEqual(sot.created_at, EXAMPLE[key])
            elif key == "job_desc":
                self.assertEqual(sot.job_description, EXAMPLE[key])
            else:
                assert_attributes_equal(self, getattr(sot, key), value)

    def test_create_sot(self):
        sot = training_job.TrainingJob(**EXAMPLE_CREATE)
        assert_attributes_equal(self, sot, EXAMPLE_CREATE)
