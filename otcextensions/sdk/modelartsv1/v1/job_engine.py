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


class JobEngine(resource.Resource):
    base_path = "/job/ai-engines"

    resources_key = "engines"

    _query_mapping = resource.QueryParameters(
        "job_type",
    )

    # capabilities
    allow_list = True

    # Properties
    #: ID of the engine selected for a training job.
    engine_id = resource.Body("engine_id", type=int)
    #: Name of the engine selected for a training job.
    engine_name = resource.Body("engine_name")
    #: Engine type of a training job1: TensorFlow5: Spark_MLlib6: Scikit
    #:  Learn9: XGBoost-Sklearn10: PyTorch17: MindSpore-GPU.
    engine_type = resource.Body("engine_type", type=int)
    #: Version of the engine selected for a training job.
    engine_version = resource.Body("engine_version")
    #: Whether the request is successful.
    is_success = resource.Body("is_success", type=bool)
