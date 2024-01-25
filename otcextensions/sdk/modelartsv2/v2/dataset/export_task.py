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
from openstack import resource


class ExportParam(resource.Resource):
    pass


class LabelStats(resource.Resource):
    pass


class Version(resource.Resource):
    #: Dataset version ID
    version_id = resource.Body("version_id", type=str)
    #: Dataset version name. The value is a string of 1 to 32 characters
    #:  consisting of only digits, letters, underscores (_),
    #:  and hyphens (-). Example value: dataset
    version_name = resource.Body("version_name", type=str)
    #: Storage format of the exported dataset.
    #:  The format is case insensitive.
    version_format = resource.Body("version_format", type=str)
    #: Parent version ID
    previous_version_id = resource.Body("previous_version_id", type=str)
    #: Status of a dataset version. Possible values are as follows:
    # 0: CREATING 1: RUNNING 2: DELETEING 3: DELETED 4: ERROR
    status = resource.Body("status", type=int)
    #: Time when a dataset is created
    create_time = resource.Body("create_time", type=int)
    #: Total number of samples
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Number of labeled samples
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Path of the manifest file of the current dataset version
    manifest_path = resource.Body("manifest_path", type=str)
    #: Whether the version is the current version
    is_current = resource.Body("is_current", type=bool)
    #: Ratio that splits the labeled data into training and
    #:  validation sets during publishing.
    train_evaluate_sample_ratio = resource.Body(
        "train_evaluate_sample_ratio", type=str
    )
    #: Whether to clear the usage information of dataset
    #:  samples. The default value is true.
    remove_sample_usage = resource.Body("remove_sample_usage", type=bool)
    #: Whether to export images to the version output directory
    #:  during publishing. The default value is false.
    export_images = resource.Body("export_images", type=bool)
    #: number of labels of a dataset version
    label_stats = resource.Body("label_stats", type=list, list_type=LabelStats)
    #: Label type of a dataset version. Possible values are as follows:
    #:  single: single-label samples
    #:  multi: multi-label samples
    #:  unlabeled: unlabeled samples
    label_type = resource.Body("label_type", type=str)


class SearchCondition(resource.Resource):
    key_sample = resource.Body("key_sample", type=str)
    label_name = resource.Body("label_name", type=dict)
    sample_time = resource.Body("sample_time", type=str)
    sample_name = resource.Body("sample_name", type=str)
    sample_dir = resource.Body("sample_dir", type=str)
    labeler = resource.Body("labeler", type=str)
    metadata = resource.Body("metadata", type=dict)


class ExportTaskSpec(resource.Resource):
    #: ID of an export task
    task_id = resource.Body("task_id", type=str)
    #: ID of the version to be exported. You need to specify the
    #:  version ID for exporting.
    version_id = resource.Body("version_id", type=str)
    #: Status of an export task. Possible values are as follows:
    #:  INIT
    #:  RUNNING
    #:  FAILED
    #:  SUCCESSED
    #:  STOPPING
    #:  STOPPED
    status = resource.Body("status", type=str)
    #: Error code of an export task.
    #:  Example: ModelArts.4311: OBS bucket does not exist.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed export task
    error_msg = resource.Body("error_msg", type=str)
    #: Progress of an export task
    progress = resource.Body("progress", type=str)
    #: Time when a task is created
    create_time = resource.Body("create_time", type=str)
    #: Save path. If data is exported to an OBS directory,
    #:  the path is an OBS path.
    path = resource.Body("path", type=str)
    #: Total number of samples to be exported
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Number of samples that are successfully exported
    finished_sample_count = resource.Body("finished_sample_count", type=int)
    #: Export Parameters
    exportParams = resource.Body("exportParams", type=ExportParam)
    #: Export type. Possible values are as follows:
    #:  0: Export only labeled data.
    #:  1: Export only unlabeled data.
    #:  2: Export all data.
    #:  3: Export data based on search criteria
    export_type = resource.Body("export_type", type=str)
    #: Storage format of the exported dataset.
    version_format = resource.Body("version_format", type=str)
    #: Format of the exported directory. This parameter is valid only
    #:  for the format of image classification datasets.
    export_format = resource.Body("export_format", type=int)


class ExportParams(resource.Resource):
    #: 	Data export destination. The value is case insensitive.
    export_dest = resource.Body("export_dest", type=str)
    #: Name of the new dataset to which data is exported
    export_new_dataset_name = resource.Body(
        "export_new_dataset_name", type=str
    )
    #: Output path for exporting data to a new dataset
    export_new_dataset_work_path = resource.Body(
        "export_new_dataset_work_path", type=str
    )
    #: Sample status based on which data is exported.
    #:  The value is case insensitive.
    sample_state = resource.Body("sample_state", type=str)
    #: List of sample IDs. Specific samples are exported based on the IDs
    samples = resource.Body("samples", type=list, list_type=str)
    #: Whether to clear hard example properties during export.
    # The default value is true, indicating that all properties of hard
    # examples are cleared.
    clear_hard_property = resource.Body("clear_hard_property", type=bool)
    search_conditions = resource.Body(
        "search_conditions", type=SearchCondition
    )


class LabelStats(resource.Resource):
    #: Label name
    name = resource.Body("name", type=str)
    #: Label type. The value range is the same as that of the dataset type.
    type = resource.Body("type", type=int)
    #: Label attribute list.
    property = resource.Body("property")
    #: Total number of labels
    count = resource.Body("count", type=int)
    #: Number of samples labeled with a label
    sample_count = resource.Body("sample_count", type=int)


class ExportTask(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/export-tasks"
    resources_key = "export_tasks"

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Dataset ID
    dataset_id = resource.URI("dataset_id", type=str)
    #: ID of an export task
    task_id = resource.Body("task_id", type=str)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call. This parameter
    #:  is not included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
    #: Status of a data import task. Possible values are as follows:
    #:  QUEUING
    #:  STARTING
    #:  RUNNING
    #:  FAILED
    #:  COMPLETED
    #:  NOT_EXIST
    status = resource.Body("status", type=str)
    #: Export path
    path = resource.Body("path", type=str)
    #: Export type. The default value is 2,
    #:  indicating that all data is exported.
    export_type = resource.Body("export_type", type=int)
    #: Number of export tasks
    total_count = resource.Body("total_count", type=int)
    #: Number of samples imported
    imported_sample_count = resource.Body("imported_sample_count", type=float)
    #: Number of labeled samples
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Task creation time
    create_time = resource.Body("create_time", type=str)
    #: ID of the version to be exported. You need to
    #:  specify the version ID for exporting.
    version_id = resource.Body("version_id", type=int)
    #: Progress of an export task
    progress = resource.Body("progress", type=str)
    #: Total number of samples to be exported
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Number of samples that are successfully exported
    finished_sample_count = resource.Body("finished_sample_count", type=int)
    #: Export Parameters
    exportParams = resource.Body("exportParams", type=ExportParams)
    #: Format of the exported directory.
    # This parameter is valid only for the format of image classification
    # datasets.
    export_format = resource.Body("export_format", type=int)
    #: Export task list
    export_tasks = resource.Body("Export task list", type=ExportTaskSpec)
    #: Error code of a failed API call. For details,
    #:  see Error Code. This parameter is not included
    #:  when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call. This parameter is
    #:  not included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
    export_params = resource.Body("export_params", type=dict)
