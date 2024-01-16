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


class Result(resource.Resource):
    #: Result of a single operation. Possible values are as follows:
    #:  true: The operation is successful.
    #:  false: The operation failed.
    success = resource.Body("success", type=bool)
    #: 	Error code.
    error_code = resource.Body("error_code", type=str)
    #: Error message. This parameter is not included
    #:  when an operation is successful.
    error_msg = resource.Body("error_msg", type=str)


class LabelProperty(resource.Resource):
    #: (Built-in attribute) Label shortcut key.
    #:  By default, this parameter is left blank.
    shortcut = resource.Body("shortcut", type=str)
    #: (Built-in attribute) Label color, which is a hexadecimal
    #:  code of the color. By default, this parameter is left blank.
    color = resource.Body("color", type=str)
    #: (Built-in attribute) Default shape of the bounding box for
    #:  object detection. By default, this parameter is left blank
    default_shape = resource.Body("default_shape", type=str)


class LabelStats(resource.Resource):
    #: Label name
    name = resource.Body("name", type=str)
    #: Label type. The value range is the same as that of the dataset type.
    type = resource.Body("type", type=int)
    #: Label attributes.
    property = resource.Body("property", type="dict")  # LabelProperty')
    #: Total number of labels
    count = resource.Body("count", type=int)


class SampleStats(resource.Resource):
    #: Number of labeled samples
    manual_annotation = resource.Body("manual_annotation", type=int)
    #: Number of unlabeled samples
    un_annotation = resource.Body("un_annotation", type=int)
    #: Number of auto labeled samples to be confirmed
    auto_annotation = resource.Body("auto_annotation", type=int)


class LabelStatistics(resource.Resource):
    base_path = "datasets/%(dataset_id)s/data-annotations/stats"  # labels'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    # resources_key = 'labels'
    # resource_key = 'label'
    dataset_id = resource.URI("dataset_id", type=str)

    #: Label Status
    # label_stats = resource.Body('label_stats', type=list,
    #                             list_type=LabelStats)
    label_stats = resource.Body("label_stats", type=LabelStats)

    #: Sample Status
    sample_stats = resource.Body("sample_stats", type=SampleStats)
    key_sample_stats = resource.Body("key_sample_stats", type=dict)


class Label(resource.Resource):
    base_path = "datasets/%(dataset_id)s/data-annotations/labels"

    resources_key = "labels"
    # resource_key = 'label'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    dataset_id = resource.URI("dataset_id", type=str)
    name = resource.Body("name", type=str)
    type = resource.Body("type", type=int)
    #: Label Status
    label_stats = resource.Body("label_stats", type=list, list_type=LabelStats)
    #: Sample Status
    sample_stats = resource.Body("sample_stats", type=SampleStats)

    #: Batch operation result
    success = resource.Body("success", type=bool)
    #: Operation result list.
    results = resource.Body("results", type=list, list_type=Result)
