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
from otcextensions.sdk.modelartsv1.v1.service import ConfigSpec


class ResultSpec(resource.Resource):
    #: Node ID.
    node_id = resource.Body("node_id")
    #: Node name.
    node_name = resource.Body("node_name")
    #: Operation type.
    operation = resource.Body("operation")
    #: Operation result.
    result = resource.Body("result", type=bool)


class ServiceLog(resource.Resource):
    base_path = "/services/%(serviceId)s/logs"

    resources_key = "logs"

    allow_list = True

    _query_mapping = resource.QueryParameters(
        "update_time",
    )

    #: Service ID.
    serviceId = resource.URI("serviceId")

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
    result_detail = resource.Body(
        "result_detail", type=list, list_type=ResultSpec
    )
    #: Number of nodes that are successfully operated. This parameter
    #:  is returned when infer_type is set to edge.
    success_num = resource.Body("success_num", type=int)
    #: Time when a service is updated, in milliseconds calculated
    #:  from 1970.1.1 0:0:0 UTC.
    update_time = resource.Body("update_time", type=int)
