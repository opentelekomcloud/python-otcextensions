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
import json

from openstack import exceptions
from openstack import resource


class NodeSpec(resource.Resource):
    #: Node architecture.
    arch = resource.Body("arch")
    #: Number of CPUs.
    cpu = resource.Body("cpu", type=int)
    #: Creation time, in the format of YYYY-MM-DDThh:mm:ss (UTC).
    created_at = resource.Body("created_at")
    #: Number of application instances deployed on a node.
    deployment_num = resource.Body("deployment_num", type=int)
    #: Description.
    description = resource.Body("description")
    #: Whether to enable the GPU.
    enable_gpu = resource.Body("enable_gpu")
    #: Number of GPUs.
    gpu_num = resource.Body("gpu_num", type=int)
    #: Host IP of a node.
    host_ips = resource.Body("host_ips", type=list)
    #: Host name of a node.
    host_name = resource.Body("host_name")
    #: Node ID.
    id = resource.Body("id")
    #: Status of a model instance on a node.
    instance_status = resource.Body("instance_status")
    #: Memory size, in MB.
    memory = resource.Body("memory", type=int)
    #: Node name.
    name = resource.Body("name")
    #: Node label.
    node_label = resource.Body("node_label")
    #: OS name.
    os_name = resource.Body("os_name")
    #: OS type.
    os_type = resource.Body("os_type")
    #: OS version.
    os_version = resource.Body("os_version")
    #: Inference URL of a node.
    predict_url = resource.Body("predict_url")
    #: Host status.
    state = resource.Body("state")
    #: Update time, in the format of YYYY-MM-DDThh:mm:ss (UTC).
    updated_at = resource.Body("updated_at")


class CustomSpec(resource.Resource):
    #: Number of required CPUs.
    cpu = resource.Body("cpu", type=float)
    #: Number of GPUs, which can be decimals.
    gpu_p4 = resource.Body("gpu_p4", type=float)
    #: Required memory capacity, in MB.
    memory = resource.Body("memory", type=int)


class ScheduleSpec(resource.Resource):
    #: Value that maps to the time unit.
    duration = resource.Body("duration", type=int)
    #: Scheduling time unit.
    time_unit = resource.Body("time_unit")
    #: Scheduling type.
    type = resource.Body("type")


class ConfigSpec(resource.Resource):
    #: Additional model deployment attribute.
    additional_properties = resource.Body("additional_properties", type=dict)
    #: ID of a dedicated resource pool.
    cluster_id = resource.Body("cluster_id")
    #: Custom specifications.
    custom_spec = resource.Body("custom_spec", type=CustomSpec)
    #: OBS path of the output data of a batch job.
    dest_path = resource.Body("dest_path")
    #: Environment variable key-value pair required for running a model.
    envs = resource.Body("envs", type=dict)
    #: Task finished time, in milliseconds calculated from 1970.
    finished_time = resource.Body("finished_time", type=int)
    #: Number of instances deployed in a model.
    instance_count = resource.Body("instance_count", type=int)
    #: Mapping between input parameters and CSV data.
    mapping_rule = resource.Body("mapping_rule", type=dict)
    #: Mapping type of the input data.
    mapping_type = resource.Body("mapping_type")
    #: Model ID.
    model_id = resource.Body("model_id")
    #: Model name.
    model_name = resource.Body("model_name")
    #: Model version.
    model_version = resource.Body("model_version")
    #: Inference path of a batch job.
    req_uri = resource.Body("req_uri")
    #: Whether auto scaling is enabled.
    scaling = resource.Body("scaling", type=bool)
    #: Model source.
    source_type = resource.Body("source_type")
    #: Resource flavor.
    specification = resource.Body("specification")
    #: OBS path of the input data of a batch job.
    src_path = resource.Body("src_path")
    #: Data source type.
    src_type = resource.Body("src_type")
    #: Task start time, in milliseconds calculated from 1970.
    start_time = resource.Body("start_time", type=int)
    #: Model status.
    status = resource.Body("status")
    #: Whether a model supports online debugging.
    support_debug = resource.Body("support_debug", type=bool)
    #: Traffic weight allocated to a model.
    weight = resource.Body("weight", type=int)


class Service(resource.Resource):
    base_path = "/services"
    resources_key = "services"

    # capabilities
    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        "cluster_id",
        "infer_type",
        "limit",
        "model_id",
        "offset",
        "order",
        "service_id",
        "service_name",
        "sort_by",
        "status",
        "workspace_id",
    )

    # Properties
    #: Access address of an inference request. This parameter is
    #:  returned when infer_type is set to real-time.
    access_address = resource.Body("access_address")
    #: Additional service attribute, which facilitates service management.
    additional_properties = resource.Body("additional_properties", type=dict)
    #: Request address of the user-defined domain name. This
    #:  parameter is returned after the domain name is bound.
    bind_access_address = resource.Body("bind_access_address")
    #: ID of the dedicated resource pool used by the real-time or batch
    #:  service.
    cluster_id = resource.Body("cluster_id")
    #: Service configuration (If a service is shared, only model_id,
    #:  model_name, and model_version are returned.
    config = resource.Body("config", type=list, list_type=ConfigSpec)
    #: Online debugging address of a real-time service.
    debug_url = resource.Body("debug_url")
    #: Service description, which contains a maximum of 100 characters.
    description = resource.Body("description")
    #: Time when a real-time service automatically stops,
    #:  in milliseconds calculated from 1970.1.1 0:0:0 UTC.
    due_time = resource.Body("due_time", type=int)
    #: Error message. When status is failed, an error message
    #:  carrying the failure cause is returned.
    error_msg = resource.Body("error_msg")
    #: Number of failed service calls.
    failed_times = resource.Body("failed_times", type=int)
    #: Inference mode. The value can be real-time, batch.
    infer_type = resource.Body("infer_type")
    #: Total number of service calls.
    invocation_times = resource.Body("invocation_times", type=int)
    #: Whether a free-of-charge flavor is used.
    is_free = resource.Body("is_free", type=bool)
    #: Whether a service is subscribed.
    is_shared = resource.Body("is_shared", type=bool)
    #: Service Name.
    name = resource.Body("name", alias="service_name")
    #: Network ID.
    network_id = resource.Body("subnet_network_id")
    #: Operation time of a request.
    operation_time = resource.Body("operation_time", type=int)
    #: User to which a service belongs.
    owner = resource.Body("owner")
    #: Deployment progress.
    progress = resource.Body("progress", type=int)
    #: Project to which a service belongs.
    project = resource.Body("project")
    #: Latest service release time, in milliseconds
    #:  calculated from 1970.1.1 0:0:0 UTC.
    publish_at = resource.Body("publish_at", type=int)
    #: Resource ID array for the resource IDs generated by the target model.
    resource_ids = resource.Body("resource_ids", type=list)
    #: ID of the VPC to which a real-time service instance is deployed.
    router_id = resource.Body("vpc_id")
    #: Service scheduling configuration, which can be configured only
    #:  for real-time services.
    schedule = resource.Body("schedule", type=list, list_type=ScheduleSpec)
    #: Security group.
    security_group_id = resource.Body("security_group_id")
    #: Service ID.
    service_id = resource.Body("service_id", alternate_id=True)
    #: Service name.
    service_name = resource.Body("service_name")
    #: Number of subscribed services.
    shared_count = resource.Body("shared_count", type=int)
    #: Service status, which can be running, deploying, concerning, failed,
    #:  stopped, or finished.
    status = resource.Body("status")
    #: Tenant to which a service belongs.
    tenant = resource.Body("tenant")
    #: Time when the service status changes.
    transition_at = resource.Body("transition_at", type=int)
    #: Time when the configuration used by a service is updated,
    #:  in milliseconds calculated from 1970.1.1 0:0:0 UTC.
    update_time = resource.Body("update_time", type=int)
    #: ID of the workspace to which a service belongs.
    workspace_id = resource.Body("workspace_id")

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data
        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.
        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body

        exceptions.raise_from_response(response, error_message=error_message)

        if has_body:
            try:
                body = response.json()
                if self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]

                for key in (
                    "model_metrics",
                    "config",
                    "apis",
                    "output_params",
                    "input_params",
                ):
                    if key in body:
                        if isinstance(body[key], str):
                            body[key] = json.loads(body[key])
                        elif key in (
                            "output_params",
                            "input_params",
                        ) and isinstance(body[key], list):
                            for param in body[key]:
                                if isinstance(param.get("param_desc"), str):
                                    param["param_desc"] = json.loads(
                                        param["param_desc"]
                                    )

                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                body.pop("self", None)

                body_attrs = self._consume_body_attrs(body)
                if self._allow_unknown_attrs_in_body:
                    body_attrs.update(body)
                    self._unknown_attrs_in_body.update(body)
                elif self._store_unknown_attrs_as_properties:
                    body_attrs = self._pack_attrs_under_properties(
                        body_attrs, body
                    )

                self._body.attributes.update(body_attrs)
                self._body.clean()
                if self.commit_jsonpatch or self.allow_patch:
                    # We need the original body to compare against
                    self._original_body = body_attrs.copy()
            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())
