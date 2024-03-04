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
from otcextensions.sdk.modelartsv1.v1 import training_job_version


EXAMPLE = {
    "job_id": 9275,
    "job_name": "matt-billing-retest-001",
    "job_desc": "test",
    "version_id": 10617,
    "version_name": "V0001",
    "pre_version_id": None,
    "resource_id": "jobbc4a1f13",
    "status": 10,
    "app_url": None,
    "boot_file_url": None,
    "create_time": 1701698401000,
    "start_time": 1701698668000,
    "is_zombie": None,
    "parameter": [
        {
            "label": "split_spec",
            "value": "train:0.8,eval:0.2",
            "required": True,
            "placeholder": "",
            "tip": {
                "content": "",
                "position": "top-left",
                "show": False,
            },
        },
    ],
    "duration": 355000,
    "spec_id": 5,
    "user_image_url": None,
    "user_command": None,
    "worker_server_num": 1,
    "data_url": "/ma-test-001/annotation/V002/V002.manifest",
    "train_url": "/matt-rgbtest/matt-billing-retest-001/",
    "dataset_id": "6KuaOYmLRz9tA2UrP4H",
    "dataset_version_id": "1EZAJDvxCuOcCqQ47ep",
    "dataset_version_name": "V002",
    "data_source": None,
    "dataset_name": "MA-UAT-001",
    "model_id": 1,
    "model_metric_list": {
        "total_metric": {
            "total_reserved_data": {},
            "total_metric_meta": {},
            "total_metric_values": {
                "recall": 0.996078,
                "precision": 0.995918,
                "f1_score": 0.995958,
                "accuracy": 0.996094,
                "top-1": 0.996094,
                "top-5": 1,
            },
        },
        "metric": [
            {
                "metric_meta": {
                    "class_name": "tulips",
                    "class_id": 4,
                },
                "metric_values": {
                    "recall": 0.980392,
                    "precision": 1,
                    "f1_score": 0.990099,
                },
                "reserved_data": {},
            },
        ],
        "images_outputs": {
            "s3://test-bucket/tulips/141479422_5a6fa1fd1b_m.jpg": {
                "real_label": ["tulips"],
                "logits": [
                    "8.085395",
                    "0.010677",
                    "-1.837408",
                    "-3.062298",
                    "-4.201297",
                ],
                "probability": [
                    "0.999621",
                    "0.000311",
                    "0.000049",
                    "0.000014",
                    "0.000005",
                ],
                "predict_label": [
                    "tulips",
                    "roses",
                    "daisy",
                    "dandelion",
                    "sunflowers",
                ],
            },
        },
    },
    "system_metric_list": {
        "interval": 1,
        "memUsage": ["0", "0", "3.58", "6.26", "11.57", "13.11", "0"],
        "recvBytesRate": [
            "0",
            "0",
            "5667968.00",
            "9162228.00",
            "9627428.00",
            "14266488.00",
            "0",
        ],
        "diskWriteRate": ["0", "0", "1.00", "0.81", "0.61", "0.31", "0"],
        "cpuUsage": ["0", "0", "18.92", "23.45", "32.25", "38.97", "0"],
        "sendBytesRate": [
            "0",
            "0",
            "1930724.00",
            "10253752.00",
            "18480064.00",
            "7347611.50",
            "0",
        ],
        "gpuUtil": ["0", "0", "0.40", "9.50", "32.50", "52.00", "0"],
        "gpuMemUsage": ["0", "0", "56.10", "70.35", "94.11", "94.11", "0"],
        "diskReadRate": [
            "0",
            "0",
            "42159.50",
            "23886.87",
            "9.00",
            "0.00",
            "0",
        ],
    },
    "log_url": None,
    "nas_type": "efs",
    "nas_share_addr": None,
    "nas_mount_path": None,
    "retrain_model_id": None,
    "volumes": None,
    "algorithm_id": None,
    "core": "8",
    "cpu": "64",
    "memory_unit": "GB",
    "gpu_num": 1,
    "gpu_type": "nvidia-v100-pcie",
    "gpu_memory_unit": "GB",
    "job_type": 1,
    "spec_code": "modelarts.vm.gpu.v100NV",
    "max_num": 1,
    # "storage": "",
    "no_resource": False,
    "npu_info": None,
    "engine_id": 500,
    "engine_type": 1000,
    "engine_name": "INNER_TensorFlow",
    "engine_version": "TF-1.8.0-python2.7",
    "pod_version": "1.8.0-cp27",
    "pool_id": "pool7e3577e3",
    "pool_name": "job-train-1v100",
    "flavor_code": "modelarts.vm.gpu.1v100NV32.pub",
    "pool_type": "SYSTEM_DEFINED",
    "flavor_type": "GPU",
    "billing": {"unit_num": 1, "code": "modelarts.vm.gpu.v100NV"},
    "flavor_info": {
        "cpu": {"arch": "x86", "core_num": 8},
        "ram": {"memory": 64, "unit": "GB"},
        "gpu": {
            "unit_num": 1,
            "product_name": "NVIDIA-V100-pcie",
            "memory": "16",
            "unit": "GB",
        },
        "max_num": 1,
        "npu_info": "",
        "npu": {
            "product_name": "",
            "unit": "GB",
            "unit_num": 0,
            "memory": 0,
            "info": "",
        },
    },
    "attributes": {"isSupportDist": "True"},
    "description": "",
    "is_free": False,
    "is_success": True,
}


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
        updated_sot_attrs = [
            "create_time",
            "parameter",
            "start_time",
            "system_metric_list",
        ]

        sot = training_job_version.TrainingJobVersion(**EXAMPLE)

        for key, value in EXAMPLE.items():
            if key not in updated_sot_attrs:
                self.assertEqual(getattr(sot, key), value)

        self.assertEqual(EXAMPLE["create_time"], sot.created_at)
        self.assertEqual(EXAMPLE["start_time"], sot.started_at)

        parameter = EXAMPLE["parameter"][0]
        sot_parameter = training_job.ParameterSpec(**parameter)
        for key, value in parameter.items():
            self.assertEqual(getattr(sot_parameter, key), value)

        self.assertEqual(
            EXAMPLE["system_metric_list"]["cpuUsage"],
            sot.system_metric_list.cpu_usage,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["memUsage"],
            sot.system_metric_list.mem_usage,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["gpuUtil"],
            sot.system_metric_list.gpu_util,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["gpuMemUsage"],
            sot.system_metric_list.gpu_mem_usage,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["diskReadRate"],
            sot.system_metric_list.disk_read_rate,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["diskWriteRate"],
            sot.system_metric_list.disk_write_rate,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["recvBytesRate"],
            sot.system_metric_list.recv_bytes_rate,
        )
        self.assertEqual(
            EXAMPLE["system_metric_list"]["sendBytesRate"],
            sot.system_metric_list.send_bytes_rate,
        )
