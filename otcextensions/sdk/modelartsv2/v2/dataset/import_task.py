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


class SourceInfo(resource.Resource):
    #: ID of an MRS cluster.
    cluster_id = resource.Body("cluster_id", type=str)
    #: Running mode of an MRS cluster. The options are as follows:
    #:  0: normal cluster 1: security cluster
    cluster_mode = resource.Body("cluster_mode", type=str)
    #: Name of an MRS cluster.
    cluster_name = resource.Body("cluster_name", type=str)
    #: Name of the database to which the table dataset is imported.
    database_name = resource.Body("database_name", type=str)
    #: HDFS path of a table dataset.
    input = resource.Body("input", type=str)
    #: IP address of your GaussDB(DWS) cluster.
    ip = resource.Body("ip", type=str)
    #: Port number of your GaussDB(DWS) cluster.
    port = resource.Body("port", type=str)
    #: DLI queue name of a table dataset.
    queue_name = resource.Body("queue_name", type=str)
    #: Subnet ID of an MRS cluster.
    subnet_id = resource.Body("subnet_id", type=str)
    #: Name of the table to which a table dataset is imported.
    table_name = resource.Body("table_name", type=str)
    #: Username, which is mandatory for GaussDB(DWS) data.
    user_name = resource.Body("user_name", type=str)
    #: User password, which is mandatory for GaussDB(DWS) data.
    user_password = resource.Body("user_password", type=str)
    #: ID of the VPC where an MRS cluster resides.
    vpc_id = resource.Body("vpc_id", type=str)


class SchemaMap(resource.Resource):
    #: Name of the destination column.
    dest_name = resource.Body("dest_name", type=str)
    #: Name of the source column.
    src_name = resource.Body("src_name", type=str)


class DataSource(resource.Resource):
    #: Data source path.
    data_path = resource.Body("data_path", type=str)
    #: Data type. The options are as follows:
    #:  0: OBS bucket (default value) 1: GaussDB(DWS)
    #:  2: DLI 3: RDS 4: MRS 5: AI Gallery 6: Inference service
    data_type = resource.Body("data_type", type=int)
    #: Schema mapping information corresponding to the table data.
    schema_maps = resource.Body("schema_maps", type=list, list_type=SchemaMap)
    #: Information required for importing a table data source.
    source_info = resource.Body("source_info", type=SourceInfo)
    #: Whether the first row in the file is a column name.
    with_column_header = resource.Body("with_column_header", type=bool)


class LabelStats(resource.Resource):
    #: Total number of labels
    count = resource.Body("count", type=int)
    #: Label name
    name = resource.Body("name", type=str)
    #: Label attribute list.
    property = resource.Body("property")
    #: Number of samples labeled with a label
    sample_count = resource.Body("sample_count", type=int)
    #: Label type. The value range is the same as that of the dataset type.
    type = resource.Body("type", type=int)


class LabelFormat(resource.Resource):
    #: Label type of text classification
    label_type = resource.Body("label_type", type=str)
    #: text_label_separator, Separator between labels.
    #:  By default, a comma (,) is used as the separator.
    text_label_separator = resource.Body("text_label_separator", type=str)
    #: Separator between the text and label.
    #:  By default, the Tab key is used as the separator.
    text_sample_separator = resource.Body("text_sample_separator", type=str)


class FileCopyProgress(resource.Resource):
    #: Number of files that have been transferred.
    file_num_finished = resource.Body("file_num_finished", type=float)
    #: Total number of files.
    file_num_total = resource.Body("file_num_total", type=float)
    #: Size of the file that has been transferred, in bytes.
    file_size_finished = resource.Body("file_size_finished", type=float)
    #: Total file size, in bytes.
    file_size_total = resource.Body("file_size_total", type=float)


class Version(resource.Resource):
    #: Number of labeled samples
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Time when a dataset is created
    create_time = resource.Body("create_time", type=int)
    #: Whether to export images to the version output directory
    #:  during publishing. The default value is false.
    export_images = resource.Body("export_images", type=bool)
    #: Whether the version is the current version
    is_current = resource.Body("is_current", type=bool)
    #: number of labels of a dataset version
    label_stats = resource.Body("label_stats", type=list, list_type=LabelStats)
    #: Label type of a dataset version. Possible values are as follows:
    #:  single: single-label samples
    #:  multi: multi-label samples
    #:  unlabeled: unlabeled samples
    label_type = resource.Body("label_type", type=str)
    #: Path of the manifest file of the current dataset version
    manifest_path = resource.Body("manifest_path", type=str)
    #: Parent version ID
    previous_version_id = resource.Body("previous_version_id", type=str)
    #: Whether to clear the usage information of dataset samples.
    #:  The default value is true.
    remove_sample_usage = resource.Body("remove_sample_usage", type=bool)
    #: Status of a dataset version. Possible values are as follows:
    # 0: CREATING 1: RUNNING 2: DELETEING 3: DELETED 4: ERROR
    status = resource.Body("status", type=int)
    #: Total number of samples
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Ratio that splits the labeled data into training and
    #:  validation sets during publishing.
    train_evaluate_sample_ratio = resource.Body(
        "train_evaluate_sample_ratio", type=str
    )
    #: Dataset version ID
    version_id = resource.Body("version_id", type=str)
    #: Format of the exported version file.
    version_format = resource.Body("version_format", type=str)
    #: Dataset version name. The value is a string of 1 to 32 characters
    # consisting of only digits, letters, underscores (_), and hyphens (-).
    # Example value: dataset
    version_name = resource.Body("version_name", type=str)


class ImportTask(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/import-tasks"

    resources_key = "import_tasks"

    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Number of labeled samples
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Task creation time
    create_time = resource.Body("create_time", type=float)
    #: Dataset ID
    dataset_id = resource.URI("dataset_id", type=str)
    #: Data source
    data_source = resource.Body("data_source", type=DataSource)
    #: Task running time, in seconds.
    elapsed_time = resource.Body("elapsed_time", type=float)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call.
    #:  This parameter is not included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
    #: Progress of file copy.
    file_statistics = resource.Body("file_statistics", type=FileCopyProgress)
    #: Number of files that have been transferred.
    finished_file_count = resource.Body("finished_file_count", type=float)
    #: Size of the file that has been transferred, in bytes.
    finished_file_size = resource.Body("finished_file_size", type=float)
    #: Import path
    import_path = resource.Body("import_path", type=str)
    #: Import type 0: Import the directory. 1: Import the manifest file.
    import_type = resource.Body("import_type", type=int)
    #: Number of samples imported
    imported_sample_count = resource.Body("imported_sample_count", type=float)
    #: Number of imported subsamples.
    imported_sub_sample_count = resource.Body(
        "imported_sub_sample_count", type=float
    )
    #: ID of a preprocessing task.
    processor_task_id = resource.Body("processor_task_id", type=str)
    #: Status of a preprocessing task.
    processor_task_status = resource.Body("processor_task_status", type=int)
    #: Status of a data import task. Possible values are as follows:
    #:  QUEUING
    #:  STARTING
    #:  RUNNING
    #:  FAILED
    #:  COMPLETED
    #:  NOT_EXIST
    status = resource.Body("status", type=str)
    #: ID of an import task
    task_id = resource.Body("task_id", type=str)
    #: Number of import tasks.
    total_file_count = resource.Body("total_file_count", type=float)
    #: Total file size, in bytes.
    total_file_size = resource.Body("total_file_size", type=float)
    #: Total number of samples to be imported
    total_sample_count = resource.Body("total_sample_count", type=float)
    #: Total number of subsamples generated from the parent samples.
    total_sub_sample_count = resource.Body(
        "total_sub_sample_count", type=float
    )
    #: Number of samples to be confirmed.
    unconfirmed_sample_count = resource.Body(
        "unconfirmed_sample_count", type=float
    )
    #: Time when a task is updated.
    update_ms = resource.Body("update_ms", type=float)
