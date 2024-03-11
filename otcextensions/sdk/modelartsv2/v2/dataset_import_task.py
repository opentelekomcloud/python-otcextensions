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
from otcextensions.sdk.modelartsv2.v2.dataset import DataSourceSpec
from otcextensions.sdk.modelartsv2.v2.dataset import LabelFormatSpec
from otcextensions.sdk.modelartsv2.v2.dataset import LabelSpec


class FileCopyProgressSpec(resource.Resource):
    #: Number of files that have been transferred.
    file_num_finished = resource.Body("file_num_finished", type=int)
    #: Total number of files.
    file_num_total = resource.Body("file_num_total", type=int)
    #: Size of the file that has been transferred, in bytes.
    file_size_finished = resource.Body("file_size_finished", type=int)
    #: Total file size, in bytes.
    file_size_total = resource.Body("file_size_total", type=int)


class DatasetImportTask(resource.Resource):
    base_path = "/datasets/%(datasetId)s/import-tasks"

    resources_key = "import_tasks"

    _query_mapping = resource.QueryParameters(
        "limit",
        "offset",
    )

    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_patch = True

    #: Dataset ID.
    datasetId = resource.URI("datasetId")

    # Properties
    #: Number of labeled samples.
    annotated_sample_count = resource.Body("annotated_sample_count", type=int)
    #: Format of the labeling information.
    annotation_format = resource.Body("annotation_format")
    #: Time when a task is created.
    create_time = resource.Body("create_time", type=int)
    #: Data source.
    data_source = resource.Body("data_source", type=DataSourceSpec)
    #: Dataset ID.
    dataset_id = resource.Body("dataset_id")
    #: Whether to import only hard examples.
    difficult_only = resource.Body("difficult_only", type=bool)
    #: Task running time, in seconds.
    elapsed_time = resource.Body("elapsed_time", type=int)
    #: Error code.
    error_code = resource.Body("error_code")
    #: Error message.
    error_msg = resource.Body("error_msg")
    #: Do not import samples containing the specified label.
    excluded_labels = resource.Body(
        "excluded_labels", type=list, list_type=LabelSpec
    )
    #: Progress of file copy.
    file_statistics = resource.Body(
        "file_statistics", type=FileCopyProgressSpec
    )
    #: Whether to import data to the final state.
    final_annotation = resource.Body("final_annotation", type=bool)
    #: Number of files that have been transferred.
    finished_file_count = resource.Body("finished_file_count", type=int)
    #: Size of the file that has been transferred, in bytes.
    finished_file_size = resource.Body("finished_file_size", type=int)
    #: Whether to import labels.
    import_annotations = resource.Body("import_annotations", type=bool)
    #: Name of the subdirectory in the dataset storage directory after import.
    import_folder = resource.Body("import_folder")
    #: Data source.
    import_origin = resource.Body("import_origin")
    #: OBS path or manifest path to be imported.
    import_path = resource.Body("import_path")
    #: Import mode.
    import_type = resource.Body("import_type", type=int)
    #: Whether to import samples.
    import_samples = resource.Body("import_samples", type=bool)
    #: Number of imported samples.
    imported_sample_count = resource.Body("imported_sample_count", type=int)
    #: Number of imported subsamples.
    imported_sub_sample_count = resource.Body(
        "imported_sub_sample_count", type=int
    )
    #: Import samples containing the specified label.
    included_labels = resource.Body(
        "included_labels", type=list, list_type=LabelSpec
    )
    #: Label format.
    label_format = resource.Body("label_format", type=LabelFormatSpec)
    #: ID of a preprocessing task.
    processor_task_id = resource.Body("processor_task_id")
    #: Status of a preprocessing task.
    processor_task_status = resource.Body("processor_task_status", type=int)
    #: Status of an import task.
    status = resource.Body("status")
    #: ID of an import task.
    task_id = resource.Body("task_id", alternate_id=True)
    #: Total number of files.
    total_file_count = resource.Body("total_file_count", type=int)
    #: Total file size, in bytes.
    total_file_size = resource.Body("total_file_size", type=int)
    #: Total number of samples.
    total_sample_count = resource.Body("total_sample_count", type=int)
    #: Total number of subsamples generated from the parent samples.
    total_sub_sample_count = resource.Body("total_sub_sample_count", type=int)
    #: Number of samples to be confirmed.
    unconfirmed_sample_count = resource.Body(
        "unconfirmed_sample_count", type=int
    )
    #: Time when a task is updated.
    update_ms = resource.Body("update_ms", type=int)
    #: Whether the first row in the file is a column name.
    with_column_header = resource.Body("with_column_header", type=bool)
