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


class Model:
    #: Model ID
    model_id = resource.Body("model_id", type=int)

    #: Model name
    model_name = resource.Body("model_name", type=str)

    #: Model usage
    model_usage = resource.Body("model_usage", type=int)

    #: Model precision
    model_precision = resource.Body("model_precision", type=str)

    #: Model size, in bytes
    model_size = resource.Body("model_size", type=float)

    #: Model training dataset
    model_train_dataset = resource.Body("model_train_dataset", type=str)

    #: Dataset format required by a model
    model_dataset_format = resource.Body("model_dataset_format", type=str)

    #: URL of the model description
    model_description_url = resource.Body("model_description_url", type=str)

    #: Running parameters of a model
    parameter = resource.Body("parameter", type=str)

    #: Time when a model is created
    create_time = resource.Body("create_time", type=int)

    #: Engine ID of a model
    engine_id = resource.Body("engine_id", type=float)

    #: Engine name of a model
    engine_name = resource.Body("engine_name", type=str)

    #: Engine version of a model
    engine_version = resource.Body("engine_version", type=str)


class BuiltinAlgorithms(resource.Resource):
    base_path = "/built-in-algorithms"
    # resource_key = 'jobs'

    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Number of job parameters displayed on each page
    per_page = resource.Body("per_page", type=int)

    #: Index of the page to be queried
    page = resource.Body("page", type=int)

    #: Sorting mode of the query
    sortBy = resource.Body("sortBy", type=str)

    #: Sorting order
    order = resource.Body("order", type=str)

    #: Search content, for example, a parameter name
    search_content = resource.Body("search_content", type=str)

    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)

    #: Error message of a failed API call
    error_message = resource.Body("error_message", type=str)

    #: Error code of a failed API call
    error_code = resource.Body("error_code", type=str)

    #: Number of models
    model_total_count = resource.Body("model_total_count", type=int)

    #: Model parameter list
    models = resource.Body("models", type=list, list_type=Model)
