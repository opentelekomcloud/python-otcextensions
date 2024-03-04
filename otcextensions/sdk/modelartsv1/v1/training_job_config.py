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
from otcextensions.sdk.modelartsv1.v1.training_job import ConfigSpec


class TrainingJobConfig(ConfigSpec):
    base_path = "/training-job-configs"

    resources_key = "configs"

    _query_mapping = resource.QueryParameters(
        "config_type",
        "limit",
        "order",
        "offset",
        "search_content",
        "sort_by",
        limit="per_page",
        offset="page",
        sort_by="sortBy",
    )

    # capabilities
    allow_create = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_list = True

    #: Name of a training job configuration.
    config_name = resource.Body("config_name")
    #: Description of a training job configuration.
    config_desc = resource.Body("config_desc")
    #: Name of a training job configuration.
    name = resource.Body("name", alias="config_name")
