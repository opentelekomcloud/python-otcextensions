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


# *************************** CLASS Configparametersofreal-time *************************************
class ConfigRealtime(resource.Resource):
    #: Model ID
    model_id = resource.Body('model_id', type=str)

    #: Traffic weight allocated to a model
    weight = resource.Body('weight', type=int)

    #: Resource specifications
    specification = resource.Body('specification', type=str)

    #: Custom specifications
    custom_spec = resource.Body('custom_spec', type=dict)

    #: Number of instances for deploying a model
    instance_count = resource.Body('instance_count', type=int)

    #: (Optional) Environment variable key-value pair required for running a model
    envs = resource.Body('envs', type=dict)

    #: ID of a dedicated resource pool
    cluster_id = resource.Body('cluster_id', type=str)


# *************************** CLASS Configparametersofbatch *************************************
class ConfigBatch(resource.Resource):
    #: Model ID
    model_id = resource.Body('model_id', type=str)

    #: Resource flavor
    specification = resource.Body('specification', type=str)

    #: Number of instances for deploying a model
    instance_count = resource.Body('instance_count', type=int)

    #: (Optional) Environment variable key-value pair required for running a model
    envs = resource.Body('envs', type=dict)

    #: Data source type
    src_type = resource.Body('src_type', type=str)

    #: OBS path of the input data of a batch job
    src_path = resource.Body('src_path', type=str)

    #: OBS path of the output data of a batch job
    dest_path = resource.Body('dest_path', type=str)

    #: Inference API called in a batch job, which is a REST API in the model image
    req_uri = resource.Body('req_uri', type=str)

    #: Mapping type of the input data
    mapping_type = resource.Body('mapping_type', type=str)

    #: Mapping between input parameters and CSV data
    mapping_rule = resource.Body('mapping_rule', type=dict)


# *************************** CLASS Scheduleparameters *************************************
class Schedule(resource.Resource):
    #: Scheduling type
    type = resource.Body('type', type=str)

    #: Scheduling time unit
    time_unit = resource.Body('time_unit', type=str)

    #: Value that maps to the time unit
    duration = resource.Body('duration', type=int)

class CustomSpec(resource.Resource):
     #: Number of required CPUs
     cpu = resource.Body('float', type=str)

     #: Required memory capacity, in MB
     memory = resource.Body('int', type=str)

     #: Number of GPUs, which can be decimals.
     gpu4 = resource.Body('float', type=str)


class ServiceConfigurationUpdate(resource.Resource):
    base_path = "/services/%(service_id)s"

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True
    service_id = resource.URI("service_id", type=str)

    #: Service description, which contains a maximum of 100 characters
    description = resource.Body('description', type=str)

    #: Service status
    status = resource.Body('status', type=str)

    #: Service configuration
    config = resource.Body('config', type=list, list_type=ConfigRealtime) ################

    #: Service scheduling configuration, which can be configured only for real-time services
    schedule = resource.Body('schedule', type=Schedule)

    #: Additional service attribute, which facilitates service management
    additional_properties = resource.Body('additional_properties', type=dict)

