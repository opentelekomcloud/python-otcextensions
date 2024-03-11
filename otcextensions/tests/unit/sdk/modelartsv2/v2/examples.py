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

DATASET = {
    "dataset_id": "dataset-id",
    "dataset_name": "dataset-name",
    "dataset_type": 0,
    "data_format": "Default",
    "next_version_num": 2,
    "status": 1,
    "data_sources": [{"data_type": 0, "data_path": "/pdinput/"}],
    "create_time": 1694604098240,
    "update_time": 1694604098240,
    "description": "",
    "current_version_id": "curr-version-id",
    "current_version_name": "V001",
    "total_sample_count": 176244,
    "annotated_sample_count": 176244,
    "unconfirmed_sample_count": 0,
    "work_path": "/pdoutput/",
    "inner_work_path": "/",
    "inner_annotation_path": "/annotation/",
    "inner_data_path": "/data/",
    "inner_log_path": "/logs/",
    "inner_temp_path": "/temp/",
    "inner_task_path": "/task/",
    "work_path_type": 0,
    "workspace_id": "0",
    "enterprise_project_id": "0",
    "workforce_task_count": 0,
    "feature_supports": ["0"],
    "managed": False,
    "import_data": False,
    "ai_project": "default-ai-project",
    "label_task_count": 1,
    "dataset_format": 0,
    "dataset_version_count": 1,
    "dataset_version": "v1",
    "content_labeling": True,
    "data_update_time": 1704703808239,
    "versions": [
        {
            "version_id": "version-id",
            "version_name": "V001",
            "version_format": "Default",
            "status": 1,
            "is_current": True,
            "train_evaluate_sample_ratio": "0.80000",
            "export_images": False,
            "extract_serial_number": False,
        }
    ],
    "labels": [
        {
            "name": "Apple__Apple_scab",
            "type": 0,
            "property": {"@modelarts:color": "", "@modelarts:shortcut": ""},
            "attributes": [],
        },
        {
            "name": "Tomato_Septoria_leaf_spot",
            "type": 0,
            "property": {"@modelarts:color": "", "@modelarts:shortcut": ""},
            "attributes": [],
        },
        {
            "name": "tulips",
            "type": 0,
            "property": {"@modelarts:color": "", "@modelarts:shortcut": ""},
            "attributes": [],
        },
    ],
}


DATASET_EXPORT_TASK = {
    "task_id": "TZMuy7OKbClkGCAc3gb",
    "path": "/test-obs/daoChu/",
    "export_type": 3,
    "version_format": "Default",
    "export_format": 2,
    "export_params": {
        "sample_state": "",
        "export_dest": "DIR",
        "clear_hard_property": True,
        "clear_difficult": False,
        "train_sample_ratio": 1.0,
        "ratio_sample_usage": False,
    },
    "status": "RUNNING",
    "progress": 0.0,
    "create_time": 1606103424662,
    "update_time": 1606103494124,
}


DATASET_IMPORT_TASK = {
    "status": "COMPLETED",
    "task_id": "gfghHSokody6AJigS5A_RHJ1zOkIoI3Nzwxj8nh",
    "dataset_id": "gfghHSokody6AJigS5A",
    "import_path": "obs://test-obs/daoLu_images/cat-rabbit/",
    "import_type": 0,
    "total_sample_count": 20,
    "imported_sample_count": 20,
    "annotated_sample_count": 20,
    "total_sub_sample_count": 0,
    "imported_sub_sample_count": 0,
    "total_file_size": 0,
    "finished_file_count": 0,
    "finished_file_size": 0,
    "total_file_count": 0,
    "update_ms": 1606114833955,
    "create_time": 1606114833874,
    "elapsed_time": 2,
}


DATASET_LABEL = {
    "name": "Cat",
    "property": {
        "@modelarts:color": "#3399ff",
        "@modelarts:default_shape": "bndbox",
    },
}

DATASET_SAMPLE = {
    "annotated_by": "human/OTC-EU-DE-000000000010000XXXXXX/dummy",
    "labels": [
        {
            "name": "Tomato_healthy",
            "property": {},
            "type": 0,
        },
    ],
    "sample_type": 0,
    "source": "https://dummydummy/testdata",
    "preview": "https://dummydummy/test",
    "sample_id": "000500f237d4c078ca64f2fd99da9828",
    "sample_status": "MANUAL_ANNOTATION",
    "sample_time": 1694457754000,
    "metadata": {
        "@modelarts:import_origin": 0,
        "@modelarts:size": [256, 256, 3],
        "@modelarts:source_image_info": "https://dummydummy/test",
    },
}


DATASET_STATISTICS = {
    "label_stats": [
        {
            "name": "daisy",
            "type": 0,
            "property": {"@modelarts:color": "#266b5e"},
            "count": 0,
            "sample_count": 0,
        },
        {
            "name": "dandelion",
            "type": 0,
            "property": {"@modelarts:color": "#1a0135"},
            "count": 0,
            "sample_count": 0,
        },
    ],
    "sample_stats": {
        "un_annotation": 500,
        "all": 500,
        "total": 500,
        "deleted": 0,
        "manual_annotation": 0,
        "auto_annotation": 0,
        "lefted": 500,
    },
    "key_sample_stats": {
        "total": 500,
        "non_key_sample": 500,
        "key_sample": 0,
    },
    "deletion_stats": {},
    "metadata_stats": {},
    "data_spliting_enable": False,
}


DATASET_VERSION = {
    "annotated_sample_count": 600,
    "create_time": 1707050585432,
    "data_path": "/path..",
    "description": "",
    "export_images": False,
    "extract_serial_number": False,
    "is_current": True,
    "label_stats": [
        {
            "name": "Potato___Early_blight",
            "type": 0,
            "property": {"@modelarts:color": "", "@modelarts:shortcut": ""},
            "attributes": [],
            "count": 300,
            "sample_count": 300,
        },
        {
            "name": "Tomato___Bacterial_spot",
            "type": 0,
            "property": {"@modelarts:color": "", "@modelarts:shortcut": ""},
            "attributes": [],
            "count": 300,
            "sample_count": 300,
        },
    ],
    "label_type": "single",
    "manifest_path": "/path..",
    "previous_version_id": "previous-version-id",
    "remove_sample_usage": False,
    "status": 1,
    "task_type": 0,
    "total_sample_count": 1800,
    "train_evaluate_sample_ratio": "1.00",
    "version_format": "Default",
    "version_id": "version-id",
    "version_name": "V0fsfsfs04",
}
