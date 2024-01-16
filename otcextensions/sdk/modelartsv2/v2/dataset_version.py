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


class LabelStats(resource.Resource):
    pass


class Version(resource.Resource):
    #: Dataset version ID
    version_id = resource.Body("version_id", type=str)
    #: Dataset version name. The value is a string of 1 to 32 characters
    #:  consisting of only digits, letters, underscores (_), and hyphens (-).
    #:  Example value: dataset
    version_name = resource.Body("version_name", type=str)
    #: Format of the exported version file.
    version_format = resource.Body("version_format", type=str)
    #: Parent version ID
    previous_version_id = resource.Body("previous_version_id", type=str)
    #: Status of a dataset version. Possible values are as follows:
    #:  0: CREATING
    #:  1: RUNNING
    #:  2: DELETEING
    #:  3: DELETED
    #:  4: ERROR
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
    #: Whether to export images to the version output directory during
    #:  publishing. The default value is false.
    export_images = resource.Body("export_images", type=bool)
    #: number of labels of a dataset version
    label_stats = resource.Body("label_stats", type=list, list_type=LabelStats)
    #: Label type of a dataset version. Possible values are as follows:
    #:  single: single-label samples
    #:  multi: multi-label samples
    #:  unlabeled: unlabeled samples
    label_type = resource.Body("label_type", type=str)


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


class DatasetVersion(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/versions"

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Version name. The value is a string of 1 to 32 characters consisting
    #:  of only digits, letters, underscores (_), and hyphens (-).
    #:  Example value: dataset.
    version_name = resource.Body("version_name", type=str)
    #: Format of the exported version file, which is case insensitive.
    version_format = resource.Body("version_format", type=str)
    #: Whether to clear the usage information of dataset samples.
    #:  The default value is true
    remove_sample_usage = resource.Body("remove_sample_usage", type=bool)
    #: Whether to export images to the version output directory during
    #:  publishing. The default value is false.
    export_images = resource.Body("export_images", type=bool)
    #: Ratio that splits the labeled data into training and validation
    #:  sets during publishing.
    train_evaluate_sample_ratio = resource.Body(
        "train_evaluate_sample_ratio", type=str
    )
    #: Whether to clear hard example properties. The default value is true.
    clear_hard_property = resource.Body("clear_hard_property", type=str)
    #: 	Dataset description. The value is a string of 0 to 256 characters.
    description = resource.Body("description", type=str)
    #: Dataset ID
    dataset_id = resource.URI("dataset_id", type=str)
    #: Version ID
    version_id = resource.Body("version_id", type=str)
    #: Error code of a failed API call. For details, see Error Code.
    #:  This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: Error message of a failed API call. This parameter is not
    #:  included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
    #: Total number of returned versions
    total_number = resource.Body("total_number", type=int)
    #: Containing mulitple Versions
    versions = resource.Body("versions", type=list, list_type=Version)
