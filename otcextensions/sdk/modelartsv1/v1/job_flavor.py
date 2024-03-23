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


class JobFlavor(resource.Resource):
    base_path = "/job/resource-specs"

    resources_key = "specs"

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        "engine_id",
        "job_type",
        "project_type",
    )

    # Properties
    #: Number of cores of the resource specifications.
    core = resource.Body("core")
    #: CPU memory of the resource specifications.
    cpu = resource.Body("cpu")
    #: Number of GPUs of the resource specifications.
    gpu_num = resource.Body("gpu_num", type=int)
    #: GPU type of the resource specifications.
    gpu_type = resource.Body("gpu_type")
    #: Interface type.
    interface_type = resource.Body("interface_type", type=int)
    #: Maximum number of nodes that can be selected.
    max_num = resource.Body("max_num", type=int)
    #: Whether the resources of the selected specifications are sufficient.
    no_resource = resource.Body("no_resource", type=bool)
    #: Type of the resource specifications.
    spec_code = resource.Body("spec_code")
    #: ID of the resource specifications.
    spec_id = resource.Body("spec_id", type=int)
    #: SSD size of a resource flavor.
    storage = resource.Body("storage")
    #: Number of pricing units.
    unit_num = resource.Body("unit_num", type=int)
