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


class SearchPropSpec(resource.Resource):
    #: Relationship between attribute values.
    op = resource.Body("op")
    #: Check the document. Search criteria of an attribute.
    props = resource.Body("props", type=dict)


class SearchLabelSpec(resource.Resource):
    #: Label name.
    name = resource.Body("name")
    #: Operation type between multiple attributes.
    op = resource.Body("op")
    #: Check the document. Label attribute, which is in the Object
    #:  format and stores any key-value pairs.
    property = resource.Body("property", type=dict)
    #: Label type.
    type = resource.Body("type", type=int)


class SearchLabelsSpec(resource.Resource):
    #: List of label search criteria.
    labels = resource.Body("labels", type=list, list_type=SearchLabelSpec)
    #: If you want to search for multiple labels, op must be specified.
    op = resource.Body("op")


class SearchConditionSpec(resource.Resource):
    #: Filter by coefficient of difficulty.
    coefficient = resource.Body("coefficient")
    #: A frame in the video.
    frame_in_video = resource.Body("frame_in_video", type=int)
    #: Whether a sample is a hard sample.
    hard = resource.Body("hard")
    #: Filter by data source.
    import_origin = resource.Body("import_origin")
    #: CT dosage, filtered by dosage.
    kvp = resource.Body("kvp")
    #: Label search criteria.
    label_list = resource.Body("label_list", type=SearchLabelsSpec)
    #: Labeler.
    labeler = resource.Body("labeler")
    #: Search by sample attribute.
    metadata = resource.Body("metadata", type=SearchPropSpec)
    #: Parent sample ID.
    parent_sample_id = resource.Body("parent_sample_id")
    #: Directory where data samples are stored (the directory must end with a
    #:  slash (/)).
    sample_dir = resource.Body("sample_dir")
    #: Search by sample name, including the file name extension.
    sample_name = resource.Body("sample_name")
    #: When a sample is added to the dataset, an index is created based on the
    #:  last modification time (accurate to day) of the sample on OBS.
    sample_time = resource.Body("sample_time")
    #: Search by confidence.
    score = resource.Body("score")
    #: DICOM layer thickness.
    slice_thickness = resource.Body("slice_thickness")
    #: DICOM scanning time.
    study_date = resource.Body("study_date")
    #: A time point in the video.
    time_in_video = resource.Body("time_in_video")


class ExportParamsSpec(resource.Resource):
    #: Whether to clear difficult.
    clear_difficult = resource.Body("clear_difficult", type=bool)
    #: Whether to clear hard example attributes.
    clear_hard_property = resource.Body("clear_hard_property", type=bool)
    #: Format of the dataset version to which data is exported.
    export_dataset_version_format = resource.Body(
        "export_dataset_version_format"
    )
    #: Name of the dataset version to which data is exported.
    export_dataset_version_name = resource.Body("export_dataset_version_name")
    #: Export destination.
    export_dest = resource.Body("export_dest")
    #: Name of the new dataset to which data is exported.
    export_new_dataset_name = resource.Body("export_new_dataset_name")
    #: Working directory of the new dataset to which data is exported.
    export_new_dataset_work_path = resource.Body(
        "export_new_dataset_work_path"
    )
    #: Whether to randomly allocate the training set and validation set based
    #:  on the specified ratio.
    ratio_sample_usage = resource.Body("ratio_sample_usage", type=bool)
    #: Sample status.
    sample_state = resource.Body("sample_state")
    #: ID list of exported samples.
    samples = resource.Body("samples", type=list)
    #: Exported search conditions.
    search_conditions = resource.Body(
        "search_conditions", type=list, list_type=SearchConditionSpec
    )
    #: Split ratio of training set and verification set during specified
    #:  version release.
    train_sample_ratio = resource.Body("train_sample_ratio")


class SearchPropSpec(resource.Resource):
    #: Relationship between attribute values.
    op = resource.Body("op")
    #: Search criteria of an attribute.
    props = resource.Body("props", type=dict)


class SearchLabelSpec(resource.Resource):
    #: Label name.
    name = resource.Body("name")
    #: Operation type between multiple attributes.
    op = resource.Body("op")
    #: Label attribute, which is in the Object format and
    #:  stores any key-value pairs.
    property = resource.Body("property", type=dict)
    #: Label type.
    type = resource.Body("type", type=int)


class SearchLabelsSpec(resource.Resource):
    #: List of label search criteria.
    labels = resource.Body("labels", type=list, list_type=SearchLabelSpec)
    #: If you want to search for multiple labels, op must be specified.
    op = resource.Body("op")


class SearchConditionSpec(resource.Resource):
    #: Filter by coefficient of difficulty.
    coefficient = resource.Body("coefficient")
    #: A frame in the video.
    frame_in_video = resource.Body("frame_in_video", type=int)
    #: Whether a sample is a hard sample.
    hard = resource.Body("hard")
    #: Filter by data source.
    import_origin = resource.Body("import_origin")
    #: CT dosage, filtered by dosage.
    kvp = resource.Body("kvp")
    #: Label search criteria.
    label_list = resource.Body("label_list", type=SearchLabelsSpec)
    #: Labeler.
    labeler = resource.Body("labeler")
    #: Search by sample attribute.
    metadata = resource.Body("metadata", type=SearchPropSpec)
    #: Parent sample ID.
    parent_sample_id = resource.Body("parent_sample_id")
    #: Directory where data samples are stored (the directory must end with a
    #:  slash (/)).
    sample_dir = resource.Body("sample_dir")
    #: Search by sample name, including the file name extension.
    sample_name = resource.Body("sample_name")
    #: When a sample is added to the dataset, an index is created based on the
    #:  last modification time (accurate to day) of the sample on OBS.
    sample_time = resource.Body("sample_time")
    #: Search by confidence.
    score = resource.Body("score")
    #: DICOM layer thickness.
    slice_thickness = resource.Body("slice_thickness")
    #: DICOM scanning time.
    study_date = resource.Body("study_date")
    #: A time point in the video.
    time_in_video = resource.Body("time_in_video")


class DatasetExportTask(resource.Resource):
    base_path = "/datasets/%(datasetId)s/export-tasks"

    resources_key = "export_tasks"

    _query_mapping = resource.QueryParameters(
        "export_type",
        "limit",
        "offset",
    )

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True

    #: Dataset ID.
    datasetId = resource.URI("datasetId")

    #: Labeling format.
    annotation_format = resource.Body("annotation_format")
    #: Time when a task is created.
    create_time = resource.Body("create_time", type=int)
    #: Dataset ID.
    dataset_id = resource.Body("dataset_id")
    #: Dataset type.
    dataset_type = resource.Body("dataset_type", type=int)
    #: Error code.
    error_code = resource.Body("error_code")
    #: Error message.
    error_msg = resource.Body("error_msg")
    #: Format of the exported directory.
    export_format = resource.Body("export_format", type=int)
    #: Parameters of a dataset export task.
    export_params = resource.Body("export_params", type=ExportParamsSpec)
    #: Export type.
    export_type = resource.Body("export_type", type=int)
    #: Number of completed samples.
    finished_sample_count = resource.Body("finished_sample_count", type=int)
    #: Export output path.
    path = resource.Body("path")
    #: Percentage of current task progress.
    progress = resource.Body("progress", type=float)
    #: Sample status.
    sample_state = resource.Body("sample_state")
    #: Prefix of the OBS path in the exported labeling file.
    source_type_header = resource.Body("source_type_header")
    #: Task status.
    status = resource.Body("status", type=int)
    #: Task ID.
    task_id = resource.Body("task_id", alternate_id=True)
    #: Total number of export tasks.
    total_count = resource.Body("total_count", type=int)
    #: Total number of samples.
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Time when a task is updated.
    update_time = resource.Body("update_time", type=int)
    #: Format of a dataset version.
    version_format = resource.Body("version_format")
    #: Dataset version ID.
    version_id = resource.Body("version_id")
    #: Whether to write the column name in the first line of the CSV file
    #:  during export.
    with_column_header = resource.Body("with_column_header", type=bool)
