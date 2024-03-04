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


class WorkerSpec(resource.Resource):
    #: Creation time.
    create_time = resource.Body("create_time", type=int)
    #: Labeling team member description.
    description = resource.Body("description")
    #: Email address of a labeling team member.
    email = resource.Body("email")
    #: Role.
    role = resource.Body("role", type=int)
    #: Current login status of a labeling team member.
    status = resource.Body("status", type=int)
    #: Update time.
    update_time = resource.Body("update_time", type=int)
    #: ID of a labeling team member.
    worker_id = resource.Body("worker_id")
    #: ID of a labeling team.
    workforce_id = resource.Body("workforce_id")


class WorkforceDescriptorSpec(resource.Resource):
    #: ID of a team labeling task.
    current_task_id = resource.Body("current_task_id")
    #: Name of a team labeling task.
    current_task_name = resource.Body("current_task_name")
    #: Whether to synchronously update auto labeling data.
    is_synchronize_auto_labeling_data = resource.Body(
        "is_synchronize_auto_labeling_data", type=bool
    )
    #: Whether to synchronize updated data, such as uploading files,
    #:  synchronizing data sources, and assigning imported unlabeled files to
    #:  team members.
    is_synchronize_data = resource.Body("is_synchronize_data", type=bool)
    #: Number of rejected samples.
    reject_num = resource.Body("reject_num", type=int)
    #: Number of persons who label each sample.
    repetition = resource.Body("repetition", type=int)
    #: List of labeling team members.
    workers = resource.Body("workers", type=list, list_type=WorkerSpec)
    #: ID of a labeling team.
    workforce_id = resource.Body("workforce_id")
    #: Name of a labeling team.
    workforce_name = resource.Body("workforce_name")


class LabelPropertySpec(resource.Resource):
    #: Default attribute: Label color, which is a hexadecimal code of the
    #:  color.
    color = resource.Body("@modelarts:color")
    #: Default attribute: Default shape of an object detection label
    #:  (dedicated attribute).
    default_shape = resource.Body("@modelarts:default_shape")
    #: Default attribute: Type of the head entity in the triplet relationship
    #:  label.
    from_type = resource.Body("@modelarts:from_type")
    #: Default attribute: The new name of the label.
    rename_to = resource.Body("@modelarts:rename_to")
    #: Default attribute: Label shortcut key.
    shortcut = resource.Body("@modelarts:shortcut")
    #: Default attribute: Type of the tail entity in the triplet relationship
    #:  label.
    to_type = resource.Body("@modelarts:to_type")


class LabelAttributeValueSpec(resource.Resource):
    #: Label attribute value ID.
    id = resource.Body("id")
    #: Label attribute value.
    value = resource.Body("value")


class LabelAttributeSpec(resource.Resource):
    #: Default value of a label attribute.
    default_value = resource.Body("default_value")
    #: Label attribute ID.
    id = resource.Body("id")
    #: Label attribute name.
    name = resource.Body("name")
    #: Label attribute type.
    type = resource.Body("type")
    #: List of label attribute values.
    values = resource.Body(
        "values", type=list, list_type=LabelAttributeValueSpec
    )


class LabelSpec(resource.Resource):
    #: Multi-dimensional attribute of a label.
    attributes = resource.Body(
        "attributes", type=list, list_type=LabelAttributeSpec
    )
    #: Label name.
    name = resource.Body("name")
    #: Basic attribute key-value pair of a label, such as color and shortcut
    #:  keys.
    property = resource.Body("property", type=LabelPropertySpec)
    #: Label type.
    type = resource.Body("type", type=int)


class LabelStatsSpec(resource.Resource):
    #: Multi-dimensional attribute of a label.
    attributes = resource.Body(
        "attributes", type=list, list_type=LabelAttributeSpec
    )
    #: Number of labels.
    count = resource.Body("count", type=int)
    #: Label name.
    name = resource.Body("name")
    #: Basic attribute key-value pair of a label, such as color and shortcut
    #:  keys.
    property = resource.Body("property", type=LabelPropertySpec)
    #: Number of samples containing the label.
    sample_count = resource.Body("sample_count", type=int)
    #: Label type.
    type = resource.Body("type", type=int)


class LabelFormatSpec(resource.Resource):
    #: Label type of text classification.
    label_type = resource.Body("label_type")
    #: Separator between labels.
    text_label_separator = resource.Body("text_label_separator")
    #: Separator between the text and label.
    text_sample_separator = resource.Body("text_sample_separator")


class DatasetVersionSpec(resource.Resource):
    #: Number of added samples.
    add_sample_count = resource.Body("add_sample_count", type=int)
    #: Number of samples with labeled versions.
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Number of labeled subsamples.
    annotated_sub_sample_count = resource.Body(
        "annotated_sub_sample_count", type=int
    )
    #: Whether to clear hard example properties during release.
    clear_hard_property = resource.Body("clear_hard_property", type=bool)
    #: Status code of a preprocessing task such as rotation and cropping.
    code = resource.Body("code")
    #: Time when a version is created.
    create_time = resource.Body("create_time", type=int)
    #: Whether to crop the image.
    crop = resource.Body("crop", type=bool)
    #: Path for storing cropped files.
    crop_path = resource.Body("crop_path")
    #: Temporary directory for executing the rotation and cropping task.
    crop_rotate_cache_path = resource.Body("crop_rotate_cache_path")
    #: Path for storing data.
    data_path = resource.Body("data_path")
    #: Sample statistics on a dataset, including the statistics on sample
    #:  metadata in JSON format.
    data_statistics = resource.Body("data_statistics", type=dict)
    #: Whether data is validated by the validation algorithm before release.
    data_validate = resource.Body("data_validate", type=bool)
    #: Number of deleted samples.
    deleted_sample_count = resource.Body("deleted_sample_count", type=int)
    #: Deletion reason statistics.
    deletion_stats = resource.Body("deletion_stats", type=dict)
    #: Description of a version.
    description = resource.Body("description")
    #: Whether to export images to the version output directory during
    #:  release.
    export_images = resource.Body("export_images", type=bool)
    #: Whether to parse the subsample number during release.
    extract_serial_number = resource.Body("extract_serial_number", type=bool)
    #: Whether to include the source data of a dataset during release.
    include_dataset_data = resource.Body("include_dataset_data", type=bool)
    #: Whether the current dataset version is used.
    is_current = resource.Body("is_current", type=bool)
    #: Label statistics list of a released version.
    label_stats = resource.Body(
        "label_stats", type=list, list_type=LabelStatsSpec
    )
    #: Label type of a released version.
    label_type = resource.Body("label_type")
    #: Input path for the manifest file cache during version release.
    manifest_cache_input_path = resource.Body("manifest_cache_input_path")
    #: Path for storing the manifest file with the released version.
    manifest_path = resource.Body("manifest_path")
    #: Task information recorded during release (for example, error
    #:  information).
    message = resource.Body("message")
    #: Number of modified samples.
    modified_sample_count = resource.Body("modified_sample_count", type=int)
    #: Number of labeled samples of parent versions.
    previous_annotated_sample_count = resource.Body(
        "previous_annotated_sample_count", type=int
    )
    #: Total samples of parent versions.
    previous_total_sample_count = resource.Body(
        "previous_total_sample_count", type=int
    )
    #: Parent version ID.
    previous_version_id = resource.Body("previous_version_id")
    #: ID of a preprocessing task such as rotation and cropping.
    processor_task_id = resource.Body("processor_task_id")
    #: Status of a preprocessing task such as rotation and cropping.
    processor_task_status = resource.Body("processor_task_status", type=int)
    #: Whether to clear the existing usage information of a dataset during
    #:  release.
    remove_sample_usage = resource.Body("remove_sample_usage", type=bool)
    #: Whether to rotate the image.
    rotate = resource.Body("rotate", type=bool)
    #: Path for storing the rotated file.
    rotate_path = resource.Body("rotate_path")
    #: Sample status.
    sample_state = resource.Body("sample_state")
    #: Status of a dataset version.
    status = resource.Body("status", type=int)
    #: Key identifier list of the dataset.
    tags = resource.Body("tags", type=list)
    #: Labeling task type of the released version, which is the same as the
    #:  dataset type.
    task_type = resource.Body("task_type", type=int)
    #: Total number of version samples.
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Total number of subsamples generated from the parent samples.
    total_sub_sample_count = resource.Body("total_sub_sample_count", type=int)
    #: Split training and verification ratio during version release.
    train_evaluate_sample_ratio = resource.Body("train_evaluate_sample_ratio")
    #: Time when a version is updated.
    update_time = resource.Body("update_time", type=int)
    #: Format of a dataset version.
    version_format = resource.Body("version_format")
    #: Dataset version ID.
    version_id = resource.Body("version_id")
    #: Dataset version name.
    version_name = resource.Body("version_name")
    #: Whether the first row in the released CSV file is a column name.
    with_column_header = resource.Body("with_column_header", type=bool)


class FieldSpec(resource.Resource):
    #: Schema description.
    description = resource.Body("description")
    #: Schema name.
    name = resource.Body("name")
    #: Schema ID.
    schema_id = resource.Body("schema_id", type=int)
    #: Schema value type.
    type = resource.Body("type")


class SourceInfoSpec(resource.Resource):
    #: ID of an MRS cluster.
    cluster_id = resource.Body("cluster_id")
    #: Running mode of an MRS cluster.
    cluster_mode = resource.Body("cluster_mode")
    #: Name of an MRS cluster.
    cluster_name = resource.Body("cluster_name")
    #: Name of the database to which the table dataset is imported.
    database_name = resource.Body("database_name")
    #: HDFS path of a table dataset.
    input = resource.Body("input")
    #: IP address of your GaussDB(DWS) cluster.
    ip = resource.Body("ip")
    #: Port number of your GaussDB(DWS) cluster.
    port = resource.Body("port")
    #: DLI queue name of a table dataset.
    queue_name = resource.Body("queue_name")
    #: Subnet ID of an MRS cluster.
    subnet_id = resource.Body("subnet_id")
    #: Name of the table to which a table dataset is imported.
    table_name = resource.Body("table_name")
    #: Username, which is mandatory for GaussDB(DWS) data.
    user_name = resource.Body("user_name")
    #: User password, which is mandatory for GaussDB(DWS) data.
    user_password = resource.Body("user_password")
    #: ID of the VPC where an MRS cluster resides.
    vpc_id = resource.Body("vpc_id")


class SchemaMapSpec(resource.Resource):
    #: Name of the destination column.
    dest_name = resource.Body("dest_name")
    #: Name of the source column.
    src_name = resource.Body("src_name")


class DataSourceSpec(resource.Resource):
    #: Data source path.
    data_path = resource.Body("data_path")
    #: Data type.
    data_type = resource.Body("data_type", type=int)
    #: Schema mapping information corresponding to the table data.
    schema_maps = resource.Body(
        "schema_maps", type=list, list_type=SchemaMapSpec
    )
    #: Information required for importing a table data source.
    source_info = resource.Body("source_info", type=SourceInfoSpec)
    #: Whether the first row in the file is a column name.
    with_column_header = resource.Body("with_column_header", type=bool)


class Dataset(resource.Resource):
    base_path = "/datasets"

    resources_key = "datasets"

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        "check_running_task",
        "contain_versions",
        "dataset_type",
        "file_preview",
        "limit",
        "offset",
        "order",
        "running_task_type",
        "search_content",
        "sort_by",
        "support_export",
        "train_evaluate_ratio",
        "version_format",
        "with_labels",
        "workspace_id",
    )

    # Properties
    #: AI Project
    ai_project = resource.Body("ai_project")
    #: Number of labeled samples in a dataset.
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Number of labeled subsamples.
    annotated_sub_sample_count = resource.Body(
        "annotated_sub_sample_count", type=int
    )
    #: Whether to enable content labeling for the speech paragraph labeling
    #:  dataset.
    content_labeling = resource.Body("content_labeling", type=bool)
    #: Time when a dataset is created.
    create_time = resource.Body("create_time", type=int)
    #: Current version ID of a dataset.
    current_version_id = resource.Body("current_version_id")
    #: Current version name of a dataset.
    current_version_name = resource.Body("current_version_name")
    #: Data format.
    data_format = resource.Body("data_format")
    #: Data source list.
    data_sources = resource.Body(
        "data_sources", type=list, list_type=DataSourceSpec
    )
    #: Sample statistics on a dataset, including the statistics on sample
    #:  metadata.
    data_statistics = resource.Body("data_statistics", type=dict)
    #: Time when a sample and a label are updated.
    data_update_time = resource.Body("data_update_time", type=int)
    #: Dataset format.
    dataset_format = resource.Body("dataset_format", type=int)
    #: Dataset ID.
    dataset_id = resource.Body("dataset_id", alternate_id=True)
    #: Dataset name.
    dataset_name = resource.Body("dataset_name")
    #: Key identifier list of a dataset, for example, ["Image","Object
    #:  detection"].
    dataset_tags = resource.Body("dataset_tags", type=list)
    #: Dataset type.
    dataset_type = resource.Body("dataset_type", type=int)
    #: Dataset version.
    dataset_version = resource.Body("dataset_version")
    #: Number of dataset versions.
    dataset_version_count = resource.Body("dataset_version_count", type=int)
    #: Number of deleted samples.
    deleted_sample_count = resource.Body("deleted_sample_count", type=int)
    #: Deletion reason statistics.
    deletion_stats = resource.Body("deletion_stats", type=dict)
    #: Dataset description.
    description = resource.Body("description")
    #: Enterprise project ID.
    enterprise_project_id = resource.Body("enterprise_project_id")
    #: Whether the dataset contains running (including initialization) tasks.
    exist_running_task = resource.Body("exist_running_task", type=bool)
    #: Whether the dataset contains team labeling tasks.
    exist_workforce_task = resource.Body("exist_workforce_task", type=bool)
    #: List of features supported by the dataset.
    feature_supports = resource.Body("feature_supports", type=list)
    #: Whether to automatically import the labeling information in the input
    #:  directory, supporting detection, image classification, and text
    #:  classification.
    import_annotations = resource.Body("import_annotations", type=bool)
    #: Whether to import data.
    import_data = resource.Body("import_data", type=bool)
    #: ID of an import task.
    import_task_id = resource.Body("import_task_id")
    #: Path for storing the labeling result of a dataset.
    inner_annotation_path = resource.Body("inner_annotation_path")
    #: Path for storing the internal data of a dataset.
    inner_data_path = resource.Body("inner_data_path")
    #: Path for storing internal logs of a dataset.
    inner_log_path = resource.Body("inner_log_path")
    #: Path for internal task of a dataset.
    inner_task_path = resource.Body("inner_task_path")
    #: Path for storing internal temporary files of a dataset.
    inner_temp_path = resource.Body("inner_temp_path")
    #: Output directory of a dataset.
    inner_work_path = resource.Body("inner_work_path")
    #: Label format information.
    label_format = resource.Body("label_format", type=LabelFormatSpec)
    #: Number of labeling tasks.
    label_task_count = resource.Body("label_task_count", type=int)
    #: Dataset label list.
    labels = resource.Body("labels", type=list, list_type=LabelSpec)
    #: Number of loading samples.
    loading_sample_count = resource.Body("loading_sample_count", type=int)
    #: Whether a dataset is hosted.
    managed = resource.Body("managed", type=bool)
    #: Dataset name.
    name = resource.Body("name", alias="dataset_name")
    #: Number of next versions of a dataset.
    next_version_num = resource.Body("next_version_num", type=int)
    #: ID list of running (including initialization) tasks.
    running_tasks_id = resource.Body("running_tasks_id", type=list)
    #: Schema list.
    schema = resource.Body("schema", type=list, list_type=FieldSpec)
    #: Dataset status.
    status = resource.Body("status", type=int)
    #: Third-party path.
    third_path = resource.Body("third_path")
    #: Total number of dataset samples.
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Total number of subsamples generated from the parent samples.
    total_sub_sample_count = resource.Body("total_sub_sample_count", type=int)
    #: Number of auto labeling samples to be confirmed.
    unconfirmed_sample_count = resource.Body(
        "unconfirmed_sample_count", type=int
    )
    #: Time when a dataset is updated.
    update_time = resource.Body("update_time", type=int)
    #: Dataset version information.
    versions = resource.Body(
        "versions", type=list, list_type=DatasetVersionSpec
    )
    #: Output dataset path, which is used to store output files such as label
    #:  files.
    work_path = resource.Body("work_path")
    #: Type of the dataset output path.
    work_path_type = resource.Body("work_path_type", type=int)
    #: Team labeling information.
    workforce_descriptor = resource.Body(
        "workforce_descriptor", type=WorkforceDescriptorSpec
    )
    #: Number of team labeling tasks of a dataset.
    workforce_task_count = resource.Body("workforce_task_count", type=int)
    #: Workspace ID.
    workspace_id = resource.Body("workspace_id")
