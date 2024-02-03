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


class ConfigSpec(resource.Resource):
    #: Model ID
    model_id = resource.Body("model_id", type=str)
    #: Traffic weight allocated to a model. This parameter is
    #:  returned when infer_type is set to real-time.
    weight = resource.Body("weight", type=int)
    #: Resource flavor. This parameter is returned
    #:  when infer_type is set to real-time.
    specification = resource.Body("specification", type=str)
    #: Number of instances deployed in a model. This parameter
    #:  is returned when infer_type is set to real-time.
    instance_count = resource.Body("instance_count", type=int)
    #: Environment variable key-value pair required for running a model
    envs = resource.Body("envs", type=dict)
    #: ID of a dedicated resource pool
    cluster_id = resource.Body("cluster_id", type=str)
    #: Model name
    model_name = resource.Body("model_name", type=str)
    #: Model version
    model_version = resource.Body("model_version", type=str)


class Log(resource.Resource):
    base_path = "/services/%(service_id)s/logs"

    resources_key = "logs"

    allow_list = True

    _query_mapping = resource.QueryParameters(
        "update_time",
    )

    #: Service ID.
    service_id = resource.URI("service_id")

    # Properties
    #: ID of a dedicated resource pool.
    cluster_id = resource.Body("cluster_id")
    #: Updated service configurations.
    config = resource.Body("config", type=list, list_type=ConfigSpec)
    #: Personalized configuration.
    extend_config = resource.Body("extend_config", type=list)
    #: Number of nodes that fail to be operated. This parameter is
    #:  returned when infer_type is set to edge.
    failed_num = resource.Body("failed_num", type=int)
    #: Update result. The value can be `SUCCESS`, `FAIL`, or `RUNNING`.
    result = resource.Body("result")
    #: Operation result details. This parameter is returned when
    #:  infer_type is set to edge.
    result_detail = resource.Body("result_detail", type=list, list_type=dict)
    #: Number of nodes that are successfully operated. This parameter
    #:  is returned when infer_type is set to edge.
    success_num = resource.Body("success_num", type=int)
    #: Time when a service is updated, in milliseconds calculated
    #:  from 1970.1.1 0:0:0 UTC.
    update_time = resource.Body("update_time", type=int)