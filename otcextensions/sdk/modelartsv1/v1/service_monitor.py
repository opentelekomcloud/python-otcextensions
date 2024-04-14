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


class ServiceMonitor(resource.Resource):
    base_path = "/services/%(service_id)s/monitor"

    resources_key = "monitors"

    allow_list = True

    _query_mapping = resource.QueryParameters(
        "node_id",
    )

    # Properties
    #: Model ID.
    model_id = resource.Body("model_id")
    #: Model name.
    model_name = resource.Body("model_name")
    #: Model Version.
    model_version = resource.Body("model_version")
    #: Total number of model instance calls.
    invocation_times = resource.Body("invocation_times", type=int)
    #: Number of failed model instance calls.
    failed_times = resource.Body("failed_times", type=int)
    #: Number of used CPUs.
    cpu_core_usage = resource.Body("cpu_core_usage", type=float)
    #: Total number of CPUs.
    cpu_core_total = resource.Body("cpu_core_total", type=float)
    #: Used memory, in MB.
    cpu_memory_usage = resource.Body("cpu_memory_usage", type=int)
    #: Total memory, in MB.
    cpu_memory_total = resource.Body("cpu_memory_total", type=int)
    #: Number used GPUs.
    gpu_usage = resource.Body("gpu_usage", type=float)
    #: Total number of GPUs.
    gpu_total = resource.Body("gpu_total", type=float)
    #: Service ID.
    service_id = resource.URI("service_id")
