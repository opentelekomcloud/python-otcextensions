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


class DatasetStatistics(resource.Resource):
    base_path = "/datasets/%(dataset_id)s/data-annotations/stats"

    # capabilities
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "email",
        "locale",
        "sample_state",
    )

    # Properties
    #: Path for storing data of a dataset.
    data_path = resource.Body("data_path")
    #: Dataset ID.
    dataset_id = resource.URI("dataset_id")
    #: Deletion Stats.
    deletion_stats = resource.Body("deletion_stats", type=dict)
    #: Label statistics grouped by labeling type.
    grouped_label_stats = resource.Body("grouped_label_stats", type=dict)
    #: Statistics on hard example reasons.
    hard_detail_stats = resource.Body("hard_detail_stats", type=dict)
    #: Whether the dataset can be split into training set and validation
    #:  set based on the sample labeling statistics.
    is_data_spliting_enabled = resource.Body("data_spliting_enable", type=bool)
    #: Statistics on hard examples.
    key_sample_stats = resource.Body("key_sample_stats", type=dict)
    #: List of label statistics.
    label_stats = resource.Body("label_stats", type=list, list_type=dict)
    #: Statistics on sample metadata, in JSON format.
    metadata_stats = resource.Body("metadata_stats", type=dict)
    #: Statistics on sample status.
    sample_stats = resource.Body("sample_stats", type=dict)
