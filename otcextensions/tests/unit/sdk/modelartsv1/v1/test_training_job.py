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


EXAMPLE_CREATE = {
    "job_name": "TestModelArtsJob3",
    "job_desc": "This is a ModelArts job",
    "workspace_id": "af261af2218841ec960b01ab3cf1a5fa",
    "config": {
        "worker_server_num": 1,
        "app_url": "/usr/app/",
        "boot_file_url": "/usr/app/boot.py",
        "parameter": [
            {"label": "learning_rate", "value": "0.01"},
            {"label": "batch_size", "value": "32"},
        ],
        "dataset_id": "38277e62-9e59-48f4-8d89-c8cf41622c24",
        "dataset_version_id": "2ff0d6ba-c480-45ae-be41-09a8369bfc90",
        "spec_id": 1,
        "engine_id": 1,
        "train_url": "/usr/train/",
        "log_url": "/usr/log/",
        "volumes": [
            {
                "nfs": {
                    "id": "43b37236-9afa-4855-8174-32254b9562e7",
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

    # def test_make_it(self):
    #    updated_sot_attrs = ["create_time"]
    #    sot = training_job.TrainingJob(**EXAMPLE)
    #    self.assertEqual(EXAMPLE["create_time"], sot.created_at)

    #    for key, value in EXAMPLE.items():
    #        if key not in updated_sot_attrs:
    #            self.assertEqual(getattr(sot, key), value)

    def test_make_create(self):
        sot = training_job.TrainingJob(**EXAMPLE_CREATE)

        for key, value in EXAMPLE_CREATE.items():
            if key not in ["config"]:
                self.assertEqual(getattr(sot, key), value)

        config = EXAMPLE_CREATE["config"]
        sot_config = training_job.ConfigSpec(**config)
        for key, value in config.items():
            if key not in ["parameter", "volumes"]:
                self.assertEqual(getattr(sot_config, key), value)

        config_parameter = EXAMPLE_CREATE["config"]["parameter"][0]
        sot_config_parameter = training_job.ParameterSpec(**config_parameter)
        for key, value in config_parameter.items():
            self.assertEqual(getattr(sot_config_parameter, key), value)

        config_volume_nfs = EXAMPLE_CREATE["config"]["volumes"][0]["nfs"]
        sot_config_volume_nfs = training_job.NfsSpec(**config_volume_nfs)
        for key, value in config_volume_nfs.items():
            self.assertEqual(getattr(sot_config_volume_nfs, key), value)

        config_volume_hostpath = EXAMPLE_CREATE["config"]["volumes"][1][
            "host_path"
        ]
        sot_config_volume_hostpath = training_job.HostPathSpec(
            **config_volume_hostpath
        )
        for key, value in config_volume_hostpath.items():
            self.assertEqual(getattr(sot_config_volume_hostpath, key), value)
