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


# ************* CLASS Config parameters *************

class ConfigSpec(resource.Resource):
    #: Model ID
    model_id = resource.Body('model_id', type=str)

    #: Resource flavor
    specification = resource.Body('specification', type=str)

    #: Number of instances for deploying a model
    instance_count = resource.Body('instance_count', type=int)

    #: (Optional) Environment variable key-value pair
    #:  required for running a model
    envs = resource.Body('envs', type=dict)

    #: Data source type
    src_type = resource.Body('src_type', type=str)

    #: OBS path of the input data of a batch job
    src_path = resource.Body('src_path', type=str)

    #: OBS path of the output data of a batch job
    dest_path = resource.Body('dest_path', type=str)

    #: Inference API called in a batch job, which
    #:  is a REST API in the model image
    req_uri = resource.Body('req_uri', type=str)

    #: Mapping type of the input data
    mapping_type = resource.Body('mapping_type', type=str)

    #: Mapping between input parameters and CSV data
    mapping_rule = resource.Body('mapping_rule', type=dict)

    #: Traffic weight allocated to a model
    weight = resource.Body('weight', type=int)

    #: Resource specifications
    specification = resource.Body('specification', type=str)

    #: Custom specifications
    custom_spec = resource.Body('custom_spec', type=dict)

    #: ID of a dedicated resource pool
    cluster_id = resource.Body('cluster_id', type=str)


# ************* CLASS Schedule Parameters *************
class ScheduleSpec(resource.Resource):
    #: Scheduling type
    type = resource.Body('type', type=str)

    #: Scheduling time unit
    time_unit = resource.Body('time_unit', type=str)

    #: Value that maps to the time unit
    duration = resource.Body('duration', type=int)


class CustomSpec(resource.Resource):
    #: Number of required CPUs
    cpu = resource.Body('cpu', type=float)

    #: Required memory capacity, in MB
    memory = resource.Body('memory', type=int)

    #: Number of GPUs, which can be decimals.
    gpu_p4 = resource.Body('gpu_p4', type=float)


class ServiceUpdate(resource.Resource):
    base_path = "/services"
    resources_key = "services"

    allow_commit = True
    service_id = resource.Body("service_id", type=str, alternate_id=True)

    #: Service description, which contains a maximum of 100 characters
    description = resource.Body('description', type=str)

    #: Service status
    status = resource.Body('status', type=str)

    #: Service configuration
    config = resource.Body('config', type=list, list_type=ConfigSpec)

    #: Service scheduling configuration, which can be configured
    #:  only for real-time services
    schedule = resource.Body('schedule', type=ScheduleSpec)

    #: Additional service attribute, which facilitates service management
    additional_properties = resource.Body('additional_properties', type=dict)
