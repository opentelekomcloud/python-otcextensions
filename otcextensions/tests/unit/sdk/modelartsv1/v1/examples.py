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

BUILT_IN_MODEL = {
    "model_id": 4,
    "model_name": "ResNet_v2_50",
    "model_usage": 1,
    "model_precision": "75.55%(top1), 92.6%(top5)",
    "model_size": 102503801,
    "model_train_dataset": "ImageNet, 1,000 classes for image classification",
    "model_dataset_format": "shape: [H>=32, W>=32, C>=1]; type: int8",
    "model_description_url": "https://github.com/....../resnet.py",
    "parameter": [
        {
            "label": "batch_size",
            "value": "4",
            "required": True,
        }
    ],
    "create_time": 1522218780025,
    "engine_id": 501,
    "engine_name": "MXNet",
    "engine_version": "MXNet-1.2.1-python2.7",
}

DEVENV = {
    "ai_project": {"id": "default-ai-project"},
    "creation_timestamp": "1686643651085",
    "description": "",
    "flavor": "modelarts.vm.cpu.2u",
    "flavor_details": {
        "name": "modelarts.vm.cpu.2u",
        "params": {
            "CPU": 2,
            "GPU": 0,
            "memory": "8GiB",
        },
        "params_extends": {
            "arch": "X86_64",
            "cpu": {
                "memory_size": "8",
                "memory_unit": "GB",
                "num": 2,
            },
        },
        "status": "onSale",
        "type": "CPU",
    },
    "id": "DE-uuid",
    "latest_update_timestamp": "1709117152833",
    "name": "fsd",
    "profile": {
        "de_type": "Notebook",
        "description": "multi engine, cpu, python 3.6 for notebook",
        "id": "eb01a452-7fb2-11ed-b1b8-0255c0a80049",
        "name": "Multi-Engine 2.0 (python3)",
        "provision": {
            "annotations": {
                "category": "Multi-Engine 2.0 (Python3)",
                "type": "system",
            },
            "spec": {
                "engine": "CCE",
                "params": {
                    "annotations": None,
                    "image_name": "mul-kernel2.0-cp36",
                    "image_tag": "3.2.0-latest-p2",
                    "namespace": "atelier",
                },
            },
            "type": "Docker",
        },
    },
    "spec": {
        "annotations": {
            "target_domain": "https://notebook.eu-de.otc.t-systems.com",
            "url": "https://...",
        },
        "auto_stop": {
            "duration": 3600,
            "enable": True,
            "prompt": True,
            "remain_time": 3336,
            "stop_timestamp": 1594891408723,
        },
        "extend_params": None,
        "extend_storage": None,
        "failed_reasons": None,
        "repository": None,
        "storage": {
            "location": {
                "path": "/home/ma-user/work",
                "volume_size": 5,
                "volume_unit": "GB",
            },
            "type": "evs",
        },
    },
    "status": "RUNNING",
    "user": {
        "id": "user-uuid",
        "name": "ops_dev_env",
    },
    "workspace": {
        "id": "0",
    },
}


JOB_FLAVOR = {
    "spec_id": 44,
    "core": "8",
    "cpu": "32",
    "gpu_num": 0,
    "gpu_type": "",
    "spec_code": "modelarts.vm.cpu.8u",
    "unit_num": 1,
    "max_num": 1,
    "storage": "",
    "interface_type": 1,
    "no_resource": False,
}


MODEL = {
    "ai_project": "default-ai-project",
    "apis": [
        {
            "method": "post",
            "url": "/",
            "input_params": {
                "type": "object",
                "properties": {"images": {"type": "file"}},
            },
            "output_params": {
                "type": "object",
                "required": [
                    "detection_classes",
                    "detection_boxes",
                    "detection_scores",
                ],
                "properties": {
                    "detection_classes": {
                        "type": "array",
                        "item": {"type": "string"},
                    },
                    "detection_boxes": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "minItems": 4.0,
                            "maxItems": 4.0,
                            "items": {"type": "number"},
                        },
                    },
                    "detection_scores": {
                        "type": "array",
                        "item": {"type": "number"},
                    },
                },
            },
            "content_type": "multipart/form-data",
        }
    ],
    "config": "{...}",
    "create_at": 1673863048731,
    "dependencies": [
        {
            "installer": "pip",
            "packages": [
                {
                    "package_name": "numpy",
                    "package_version": "1.17.0",
                    "restraint": "EXACT",
                },
                {
                    "package_name": "h5py",
                    "package_version": "2.8.0",
                    "restraint": "EXACT",
                },
                {
                    "package_name": "Pillow",
                    "package_version": "5.2.0",
                    "restraint": "EXACT",
                },
                {
                    "package_name": "scipy",
                    "package_version": "1.2.1",
                    "restraint": "EXACT",
                },
                {
                    "package_name": "resampy",
                    "package_version": "0.2.1",
                    "restraint": "EXACT",
                },
                {
                    "package_name": "scikit-learn",
                    "package_version": "0.22.2",
                    "restraint": "EXACT",
                },
            ],
        }
    ],
    "execution_code": "https://...",
    "image_address": "swr.eu-de.otc.t-systems.com/...",
    "input_params": [
        {
            "url": "/",
            "method": "post",
            "param_name": "images",
            "param_type": "file",
            "param_desc": '{"type":"file"}',
        }
    ],
    "install_type": ["real-time", "batch"],
    "market_flag": False,
    "model_algorithm": "object_detection",
    "model_id": "model-id",
    "model_metrics": "{...}",
    "model_name": "MA_UAT_002_ExeML_c2dd3f46",
    "model_size": 175791900,
    "model_source": "auto",
    "model_status": "published",
    "model_type": "TensorFlow",
    "model_version": "0.2.6",
    "output_params": [
        {
            "url": "/",
            "method": "post",
            "param_name": "detection_classes",
            "param_type": "array",
            "param_desc": '{"type":"array","item":{"type":"string"}}',
        },
        {
            "url": "/",
            "method": "post",
            "param_name": "detection_scores",
            "param_type": "array",
            "param_desc": '{"type":"array","item":{"type":"number"}}',
        },
    ],
    "owner": "owner-id",
    "project": "project-id",
    "publishable_flag": False,
    "runtime": "tf1.13-python3.7-cpu",
    "source_location": "https://train_url...",
    "source_type": "auto",
    "specification": {},
    "tenant": "tenant-id",
    "tunable": False,
    "workspace_id": "0",
}

SERVICE = {
    "access_address": "https://access_address",
    "additional_properties": {},
    "config": [
        {
            "model_id": "model-uuid",
            "model_name": "model-name",
            "model_version": "0.0.1",
            "source_type": "auto",
            "specification": "modelarts.vm.high.p3",
            "custom_spec": {},
            "status": "ready",
            "weight": 100,
            "instance_count": 1,
            "scaling": False,
            "envs": {},
            "additional_properties": {},
            "support_debug": False,
        }
    ],
    "description": "Created by Exeml project(name: exeML-aqi).",
    "failed_times": 3,
    "infer_type": "real-time",
    "invocation_times": 5,
    "is_free": False,
    "is_shared": False,
    "operation_time": 1705621491068,
    "owner": "owner-uuid",
    "progress": 100,
    "project": "project-uuid",
    "publish_at": 1691908601470,
    "service_id": "service-uuid",
    "service_name": "exeML-aqi_ExeML_1691908601350529540",
    "shared_count": 0,
    "status": "running",
    "tenant": "tenant-uuid",
    "transition_at": 1696333731658,
    "update_time": 1691908601470,
    "workspace_id": "0",
}

SERVICE_CLUSTER = {
    "cluster_id": "cluster-uuid",
    "cluster_name": "pool-a1cf",
    "tenant": "tenant-uuid",
    "project": "project-uuid",
    "owner": "owner-uuid",
    "created_at": 1658743383618,
    "status": "running",
    "allocatable_cpu_cores": 7.06,
    "allocatable_memory": 27307.0,
    "allocatable_gpus": 0.0,
    "charging_mode": "postpaid",
    "max_node_count": 50,
    "nodes": {
        "specification": "modelarts.vm.cpu.8ud",
        "count": 1,
        "available_count": 1,
    },
    "services_count": {"realtime_count": 0, "batch_count": 0},
}

SERVICE_EVENT = {
    "occur_time": 1562597251764,
    "event_type": "normal",
    "event_info": "start to deploy service",
}

SERVICE_FLAVOR = {
    "specification": "modelarts.vm.gpu.v100",
    "billing_spec": "modelarts.vm.gpu.v100",
    "is_open": True,
    "spec_status": "normal",
    "is_free": False,
    "over_quota": False,
    "extend_params": 1,
}

SERVICE_LOG = {
    "config": [
        {
            "model_id": "f565ac47-6239-4e8c-b2dc-0665dc52e302",
            "model_name": "model-demo",
            "model_version": "0.0.1",
            "specification": "modelarts.vm.cpu.2u",
            "custom_spec": {},
            "weight": 100,
            "instance_count": 1,
            "scaling": False,
            "envs": {},
            "cluster_id": "2c9080f86d37da64016d381fe5940002",
        }
    ],
    "extend_config": [],
    "update_time": 1586250930708,
    "result": "RUNNING",
    "cluster_id": "2c9080f86d37da64016d381fe5940002",
}

SERVICE_MONITOR = {
    "model_id": "xxxx",
    "model_name": "minst",
    "model_version": "1.0.0",
    "invocation_times": 50,
    "failed_times": 1,
    "cpu_core_usage": 2.4,
    "cpu_core_total": 4,
    "cpu_memory_usage": 2011,
    "cpu_memory_total": 8192,
    "gpu_usage": 0.6,
    "gpu_total": 1,
}

TRAINING_JOB = {
    "job_id": 9446,
    "job_name": "ma-testing",
    "version_id": 10818,
    "status": 10,
    "create_time": 1704448084000,
    "duration": 54793000,
    "job_desc": "This is a ModelArts job",
    "version_count": 1,
    "user": {"name": "userAbc"},
}

TRAINING_JOB_CONFIG = {
    "spec_code": "modelarts.vm.gpu.v100",
    "user_image_url": "100.125.5.235:20202/jobmng/custom-cpu-base:1.0",
    "user_command": "bash -x /home/work/run_train.sh python \
                /home/work/user-job-dir/app/mnist/mnist_softmax.py \
                --data_url /home/work/user-job-dir/app/mnist_data",
    "dataset_version_id": "2ff0d6ba-c480-45ae-be41-09a8369bfc90",
    "engine_name": "TensorFlow",
    "is_success": True,
    "nas_mount_path": "/home/work/nas",
    "worker_server_num": 1,
    "nas_share_addr": "192.168.8.150:/",
    "train_url": "/test/minst/train_out/out1/",
    "nas_type": "nfs",
    "spec_id": 4,
    "parameter": [{"label": "learning_rate", "value": 0.01}],
    "log_url": "/usr/log/",
    "config_name": "config123",
    "app_url": "/usr/app/",
    "create_time": 1559045426000,
    "dataset_id": "38277e62-9e59-48f4-8d89-c8cf41622c24",
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
    "cpu": "64",
    "model_id": 4,
    "boot_file_url": "/usr/app/boot.py",
    "dataset_name": "dataset-test",
    "pool_id": "pool9928813f",
    "config_desc": "This is a config desc test",
    "gpu_num": 1,
    "data_source": [{"type": "obs", "data_url": "/test/minst/data/"}],
    "pool_name": "p100",
    "dataset_version_name": "dataset-version-test",
    "core": "8",
    "engine_type": 1,
    "engine_id": 3,
    "engine_version": "TF-1.8.0-python2.7",
    "data_url": "/test/minst/data/",
}

TRAINING_JOB_VERSION = {
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

VISUALIZATION_JOB = {
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
