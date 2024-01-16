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
import uuid

EXAMPLE_DEVENV = {
    "ai_project": {"id": "default-ai-project"},
    "creation_timestamp": "1594887749962",
    "description": "",
    "flavor": "modelarts.bm.gpu.v100NV32",
    "flavor_details": {
        "name": "modelarts.bm.gpu.v100NV32",
        "params": {
            "CPU": 8,
            "GPU": 1,
            "gpu_type": "v100NV32",
            "memory": "64GiB",
        },
        "status": "onSale",
        "type": "GPU",
    },
    "id": "DE-7d558ef8-c73d-11ea-964c-0255ac100033",
    "latest_update_timestamp": "1594888070775",
    "name": "notebook-c6fd",
    "profile": {
        "de_type": "Notebook",
        "description": "multi engine, gpu, python 3.6 for notebook",
        "flavor_type": "GPU",
        "id": "Multi-Engine 1.0 (python3)-gpu",
        "name": "Multi-Engine 1.0 (python3)-gpu",
        "provision": {
            "annotations": {
                "category": "Multi-Engine 1.0 (python3)",
                "type": "system",
            },
            "spec": {
                "engine": "CCE",
                "params": {
                    "annotations": None,
                    "image_name": "mul-kernel-gpu-cuda-cp36",
                    "image_tag": "2.0.5-B003",
                    "namespace": "atelier",
                },
            },
            "type": "Docker",
        },
    },
    "spec": {
        "annotations": {
            "target_domain": "https://xxx",
            "url": "https://xxx:32000/modelarts/hubv100/notebook",
        },
        "auto_stop": {
            "duration": 3600,
            "enable": True,
            "prompt": True,
            "remain_time": 3336,
            "stop_timestamp": 1594891408723,
        },
        "extend_params": None,
        "failed_reasons": None,
        "repository": None,
        "extend_storage": None,
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
    "user": {"id": "15dda26361214ca2a5953917d2f48ffb", "name": "ops_dev_env"},
    "workspace": {"id": "0"},
}


EXAMPLE_MODEL = {
    "model_id": "10eb0091-887f-4839-9929-cbc884f1e20e",
    "create_at": 123456,
    "model_name": "mnist",
    "model_version": "1.0.0",
    "runtime": "python2.7",
    "tenant": "6d28e85aa78b4e1a9b4bd83501bcd4a1",
    "project": "d04c10db1f264cfeb1966deff1a3527c",
    "owner": "6d28e85aa78b4e1a9b4bd83501bcd4a1",
    "source_location": "https://models.obs.xxxx.com/mnist",
    "model_type": "TensorFlow",
    "model_size": 5633481,
    "model_status": "published",
    "execution_code": "https://testmodel.obs.xxxx.com/customize_service.py",
    "image_address": "dummy-address",
    "input_params": [
        {
            "url": "/",
            "method": "post",
            "protocol": "http",
            "param_name": "data",
            "param_type": "object",
            "param_desc": '{"type":"object","properties":'
            '{"req_data":{"items":[{"type":'
            '"object","properties":{}}],"type":'
            '"array"}}}',
        }
    ],
    "output_params": [
        {
            "url": "/",
            "method": "post",
            "protocol": "http",
            "param_name": "data",
            "param_type": "object",
            "param_desc": '{"type":"object","properties":'
            '{"resp_data":{"type":"array",'
            '"items":[{"type":"object",'
            '"properties":{}}]}}}',
        }
    ],
    "dependencies": [
        {
            "installer": "pip",
            "packages": [
                {
                    "package_name": "pkg1",
                    "package_version": "1.0.1",
                    "restraint": "ATLEAST",
                }
            ],
        }
    ],
    "model_metrics": '{"f1":0.52381,"recall":0.666667,'
    '"precision":0.466667,"accuracy":0.625}',
    "apis": '[{"protocol":"http","method":"post",'
    '"url":"/","input_params":{"type":"object",'
    '"properties":{"data":{"type":"object","properties":'
    '{"req_data":{"items":[{"type":"object","properties":'
    '{}}],"type":"array"}}}}},"output_params":{"type":'
    '"object","properties":{"data":{"type":"object",'
    '"properties":{"resp_data":{"type":"array",'
    '"items":[{"type":"object","properties":{}}]}}}}}}]',
    "model_labels": [],
    "labels_map": {"labels": []},
    "workspace_id": "0",
    "install_type": ["realtime", "batch"],
    "specification": {},
    "config": '{"model_algorithm": "image_classification", '
    '"model_source": "auto", "tunable": false, '
    '"downloadable_flag": true, "algorithm": '
    '"resnet_v2_50,mobilenet_v1", "metrics": '
    '{"f1": 0.912078373015873, "recall": 0.9125, '
    '"precision": 0.9340277777777778, "accuracy": '
    '0.263250724969475}, "model_type": "TensorFlow", '
    '"runtime": "tf1.13-python3.6-cpu", "apis": '
    '[{"protocol": "https", "url": "/", "method": '
    '"post", "request": {"data": {"type": "object", '
    '"properties": {"images": {"type": "file"}}}, '
    '"Content-type": "multipart/form-data"}, "response": '
    '{"data": {"type": "object", "required": '
    '["predicted_label", "scores"], "properties": '
    '{"predicted_label": {"type": "string"}, "scores": '
    '{"type": "array", "items": {"type": "array", '
    '"minItems": 2, "maxItems": 2, "items": [{"type": '
    '"string"}, {"type": "number"}]}}}}, "Content-type": '
    '"multipart/form-data"}}], "dependencies": [{"installer": '
    '"pip", "packages": [{"package_name": "numpy", '
    '"package_version": "1.17.0", "restraint": "EXACT"}, '
    '{"package_name": "h5py", "package_version": "2.8.0", '
    '"restraint": "EXACT"}, {"package_name": "Pillow", '
    '"package_version": "5.2.0", "restraint": "EXACT"}, '
    '{"package_name": "scipy", "package_version": "1.2.1", '
    '"restraint": "EXACT"}, {"package_name": "resampy", '
    '"package_version": "0.2.1", "restraint": "EXACT"}, '
    '{"package_name": "scikit-learn", "package_version": '
    '"0.19.1", "restraint": "EXACT"}]}]}',
}


EXAMPLE_SERVICE = {
    "service_id": "f76f20ba-78f5-44e8-893a-37c8c600c02f",
    "service_name": "service-demo",
    "tenant": "xxxxx",
    "project": "xxxxx",
    "owner": "xxxxx",
    "publish_at": 1585809231902,
    "update_time": 1585809358259,
    "infer_type": "real-time",
    "status": "running",
    "progress": 100,
    "access_address": "https://xxxxx.apigw.xxxxx/",
    "cluster_id": "088458d9-5755-4110-97d8-1d21065ea10b",
    "workspace_id": "0",
    "additional_properties": {},
    "is_shared": False,
    "invocation_times": 0,
    "failed_times": 0,
    "shared_count": 0,
    "operation_time": 1586249085447,
    "config": [
        {
            "model_id": "044ebf3d-8bf4-48df-bf40-bad0e664c1e2",
            "model_name": "jar-model",
            "model_version": "1.0.1",
            "specification": "custom",
            "custom_spec": {},
            "status": "notReady",
            "weight": 100,
            "instance_count": 1,
            "scaling": False,
            "envs": {},
            "additional_properties": {},
            "support_debug": False,
        }
    ],
    "transition_at": 1585809231902,
    "is_free": False,
}


EXAMPLE_TRAINING_JOB = {
    "is_success": True,
    "job_id": "10",
    "job_name": "TestModelArtsJob",
    "status": "1",
    "create_time": "1524189990635",
    "version_id": "10",
    "version_name": "V0001",
    "resource_id": "jobafd08896",
}


EXAMPLE_VISUALIZATION_JOB = {
    "duration": 33000,
    "service_url": "https://XXX/model197/",
    "job_name": "apiTest-11",
    "create_time": 1565149736000,
    "train_url": "/wph-test/zl-test/Flowers-Set/ApiTest/",
    "job_id": 197,
    "job_desc": "ModelArts API Dialtest",
    "resource_id": uuid.uuid4().hex,
    "remaining_duration": None,
    "is_success": True,
    "status": 7,
}


EXAMPLE_TRAINING_JOB_VERSION = {
    "status": 11,
    "is_success": None,
    "error_msg": None,
    "error_code": None,
    "job_name": None,
    "version_id": 8783,
    "create_time": 1678184644000.0,
    "resource_id": "job004983f1",
    "version_name": "V0001",
    "job_desc": None,
    "version_count": None,
    "versions": None,
    "job_total_count": None,
    "job_count_limit": None,
    "jobs": None,
    "quotas": None,
    "pre_version_id": None,
    "engine_type": 1001,
    "engine_name": "INNER_MXNET",
    "engine_id": 501,
    "engine_version": "MXNet-1.2.1-python2.7",
    "app_url": None,
    "boot_file_url": None,
    "parameter": [
        {"label": "num_classes", "value": "5"},
        {"label": "lr", "value": "0.0001"},
        {"label": "split_spec", "value": "0.8"},
        {"label": "wd", "value": "0.0005"},
        {"label": "mom", "value": "0.9"},
        {"label": "eval_frequence", "value": "1"},
    ],
    "duration": 264000.0,
    "spec_id": 5,
    "core": 8,
    "cpu": 64,
    "gpu_num": 1,
    "gpu_type": "nvidia-v100-pcie",
    "worker_server_num": 1,
    "data_url": "test-data-url",
    "train_url": "test-train-url",
    "log_url": "/modelarts-uat/uat_training/log/",
    "dataset_version_id": "8RATpUqosOatNOGBr6E",
    "dataset_id": "HvC9LfRAkqNJJeW1KN4",
    "data_source": None,
    "user_image_url": None,
    "user_command": None,
    "model_id": 5,
    "model_metric_list": "{}",
    "system_metric_list": '{"cpuUsage":[-1],"memUsage":[-1],"gpuUtil":[-1]}',
    "dataset_name": "ImageNet-Flowers",
    "dataset_version_name": "V032",
    "spec_code": None,
    "start_time": 1678184645000.0,
    "volumes": None,
    "pool_id": "pool7e3577e3",
    "pool_name": "job-train-1v100",
    "nas_mount_path": None,
    "nas_share_addr": None,
    "nas_type": "efs",
    "id": 8783,
    "name": None,
}
