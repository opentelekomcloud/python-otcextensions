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


class Sample(resource.Resource):
    #: File description path. The value starting with https:// or
    #:  http:// indicates the link address, and the value starting
    #:  with content:// indicates the text.
    url = resource.Body("data_type", type=str)
    #: Sample size
    size = resource.Body("data_path", type=int)
    #: Time when a dataset is created
    create_time = resource.Body("create_time", type=float)


class DataSource(resource.Resource):
    #: Data source type. Possible values are as follows: 0: OBS
    data_type = resource.Body("data_type", type=int)
    #: Path of the data source. The value is a string of 3 to 1,024 characters.
    data_path = resource.Body("data_path", type=str)


class Label(resource.Resource):
    #: Label name The value can contain 1 to 32 characters, including Chinese
    #:  characters, digits, letters, underscores (_), and hyphens (-).
    name = resource.Body("name", type=str)
    #: Label type. The value range is the same as that of the dataset type.
    # If this parameter is not passed, the current dataset type is used by
    # default.
    type = resource.Body("type", type=int)
    #: Label attributes.
    property = resource.Body("property", type=dict)


class LabelFormat(resource.Resource):
    label_type = resource.Body("label_type", type=str)
    text_sample_separator = resource.Body("text_sample_separator", type=str)
    text_label_separator = resource.Body("text_label_separator", type=str)


class Dataset(resource.Resource):
    base_path = "/datasets"

    resources_key = "datasets"
    # resource_key = 'dataset'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    # Properties
    #: Dataset name. The value is a string of 1 to 100 characters
    #:  consisting of only digits, letters,
    # underscores (_), and hyphens (-).
    dataset_name = resource.Body("dataset_name", type=str)
    # Dataset type. Possible values are as follows:
    # 0: image classification
    # 1: object detection
    # 100: text classification
    # 101: named entity recognition
    # 102: text triplet
    # 200: sound classification
    # 201: speech content
    # 202: speech start and end points
    # 900: custom format
    dataset_type = resource.Body("dataset_type", type=int)
    #: Input dataset path, which is used to synchronize source data (such as
    #:  images, text files, and audio files) in the directory and its
    #:  subdirectories to the dataset.
    data_sources = resource.Body("data_sources", type=list)
    #: Output dataset path, which is used to store output files such
    #:  as label files. The format is /Bucket name/File path.
    work_path = resource.Body("work_path", type=str)
    #: For details, see data_type
    work_path_type = resource.Body("work_path_type", type=int)
    #: This field is mandatory for text datasets (such as datasets of text
    #:  classification and named entity recognition).
    #:  Labels need to be defined.
    labels = resource.Body("labels", type=list)
    #: Dataset description. The value is a string of 0 to 256 characters.
    #:  Special characters !<>=&"' are not allowed. By default, this parameter
    #:  is left blank
    description = resource.Body("description", type=str)
    #: Whether to synchronize the labels in the input path when creating
    #:  an object detection or image classification dataset.
    #:  The default value is true.
    import_annotations = resource.Body("import_annotations", type=bool)
    #: Label format information. This parameter is used only when a text
    #:  classification dataset is created.
    label_format = resource.Body("label_format")
    #: Workspace ID. If no workspace is created, the default value is 0.
    #:  If a workspace is created and used, use the actual value.
    workspace_id = resource.Body("workspace_id", type=str)
    #: Data source type. Possible values are as follows: 0: OBS
    data_type = resource.Body("data_type", type=int)
    #: Path of the data source. The value is a string of 3 to 1,024 characters.
    #:  When data_type is 0, that is, the type is OBS, the format is /Bucket
    #:  name/File path.
    data_path = resource.Body("data_path", type=str)
    #: Label name The value can contain 1 to 32 characters, including
    #:  Chinese characters, digits, letters, underscores (_), and hyphens (-).
    name = resource.Body("name", type=str)
    #: Label type. The value range is the same as that of the dataset type.
    #:  If this parameter is not passed, the current dataset type is used by
    #:  default.
    type = resource.Body("type", type=int)
    #: If no built-in or custom attribute needs to be set for labels, this
    #:  field can be omitted or left blank (the parameter value is {}).
    property = resource.Body("LabelProperty", type=list)
    #: Dataset ID
    dataset_id = resource.Body("dataset_id", type=str)
    #: Error code of a failed API call. For details, see Error Code.
    #:  This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call. This parameter is not included
    #:  when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)

    #: Dataset status. Possible values are as follows:
    #: 0: CREATING
    #: 1: RUNNING
    #: 2: DELETEING
    #: 3: DELETED
    #: 4: ERROR
    #: 5: SYNCING
    #: 6: PUBLISHING
    status = resource.Body("status", type=int)
    #: ID of the next version
    next_version_num = resource.Body("next_version_num", type=int)
    #: Time when a dataset is created
    create_time = resource.Body("create_time", type=float)
    #: Time when a dataset is modified
    update_time = resource.Body("update_time", type=float)
    #: Version ID of the current dataset
    current_version_id = resource.Body("current_version_id", type=str)
    #: Version of the current dataset
    current_version_name = resource.Body("current_version_name", type=str)
    #: Total number of samples
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Number of labeled samples
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Enterprise project ID
    enterprise_project_id = resource.Body("enterprise_project_id", type=str)
    #: Whether the dataset contains running (including initialization) tasks
    existRunningTask = resource.Body("existRunningTask", type=bool)
    #: List of features supported by the dataset.
    # The default value is 0, indicating that the size of OBS files is
    # restricted
    feature_supports = resource.Body(
        "feature_supports", type=list, list_type=str
    )
    #: ID of a running task. There may be multiple running tasks.
    running_tasks_id = resource.Body(
        "running_tasks_id", type=list, list_type=str
    )
    #: Whether to import data. The default value is false.
    import_data = resource.Body("import_data", type=bool)
    #: Total number of data records which meet the criteria.
    total_number = resource.Body("total_number", type=int)
    #: File description path. The value starting with https:// or
    #:  http:// indicates the link address, and the value starting
    #:  with content:// indicates the text.
    url = resource.Body("url", type=str)
    #: Sample size
    size = resource.Body("size", type=int)
    #: Containing the following attributes: url, size, create_time
    samples = resource.Body("samples", type=list, list_type=Sample)
    data_format = resource.Body("data_format", type=str)
    unconfirmed_sample_count = resource.Body(
        "unconfirmed_sample_count", type=int
    )

    inner_work_path = resource.Body("inner_work_path", type=str)
    inner_annotation_path = resource.Body("inner_annotation_path", type=str)
    inner_data_path = resource.Body("inner_data_path", type=str)
    inner_log_path = resource.Body("inner_log_path", type=str)
    inner_temp_path = resource.Body("inner_temp_path", type=str)
    inner_task_path = resource.Body("inner_task_path", type=str)
    workforce_task_count = resource.Body("workforce_task_count", type=int)
    managed = resource.Body("managed", type=bool)
    label_task_count = resource.Body("label_task_count", type=int)
    ai_project = resource.Body("ai_project", type=str)
    dataset_format = resource.Body("dataset_format", type=int)
    dataset_version_count = resource.Body("dataset_version_count", type=int)
    content_labeling = resource.Body("content_labeling", type=bool)
    dataset_version = resource.Body("dataset_version", type=str)
    add_tags = resource.Body("add_tags", type=list, list_type=dict)
