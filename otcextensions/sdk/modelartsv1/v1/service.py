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


class Service(resource.Resource):
    base_path = "/services"
    resources_key = "services"

    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    _query_mapping = resource.QueryParameters(
        "service_id",
        "service_name",
        "model_id",
        "cluster_id",
        "workspace_id",
        "infer_type",
        "status",
        "offset",
        "limit",
        "sort_by",
        "order",
    )

    #: Properties
    #: Service name. The value can contain 1 to 64 visible characters,
    #:  including Chinese characters.
    service_name = resource.Body("service_name", type=str)
    #: Service description, which contains a maximum of 100 characters.
    #:  By default, this parameter is left blank.
    description = resource.Body("description", type=str)
    #: Inference mode. The value can be real-time, batch.
    #:  real-time: real-time service. The service keeps running.
    #:  batch: batch service, which can be configured as tasks to run in
    #:  batches. When the tasks are completed, the service stops
    #:  automatically.
    infer_type = resource.Body("infer_type", type=str)
    #: ID of the workspace to which a service belongs.
    #:  The default value is 0, indicating the default workspace.
    workspace_id = resource.Body("workspace_id", type=str)
    #: ID of the VPC to which a real-time service instance is deployed.
    #:  By default, this parameter is left blank.
    router_id = resource.Body("vpc_id", type=str)
    #: ID of a subnet. By default, this parameter is left blank.
    network_id = resource.Body("subnet_network_id", type=str)
    #: Security group. By default, this parameter is left blank.
    #:  This parameter is mandatory when vpc_id is configured.
    security_group_id = resource.Body("security_group_id", type=str)
    #: ID of a dedicated cluster. This parameter is left blank by default,
    #:  indicating that no dedicated cluster is used.
    cluster_id = resource.Body("cluster_id", type=str)
    #: Model running configuration. If infer_type is batch,
    #:  you can configure only one model.
    config = resource.Body("config", type=list, list_type=dict)
    #: Service scheduling configuration, which can be configured only
    #:  for real-time services. By default, this parameter is not used.
    schedule = resource.Body("schedule", type=list, list_type=dict)
    #: Additional service attribute. If this parameter is not set,
    #:  no value is returned.
    additional_properties = resource.Body("additional_properties", type=dict)

    #: Start page of the paging list. Default value: 0
    offset = resource.Body("offset", type=int)
    #: Maximum number of records returned on each page. Default value: 1000
    limit = resource.Body("limit", type=int)
    #: Total number of services that meet the search criteria when no
    #:  paging is implemented
    total_count = resource.Body("total_count", type=int)
    #: Number of services in the query result. If offset and limit are not set,
    #: the values of count and total are the same.
    count = resource.Body("count", type=int)
    #: Collection of the queried services. For details, see Table 4.
    services = resource.Body("services", type=list)
    tenant = resource.Body("tenant", type=str)

    #: Service ID
    service_id = resource.Body("service_id", type=str)
    #: Error message. When status is failed, an error message
    #:  carrying the failure cause is returned.
    error_msg = resource.Body("error_msg", type=str)
    #: Access address of an inference request. This parameter is
    #:  returned when infer_type is set to real-time.
    access_address = resource.Body("access_address", type=str)
    #: Request address of the user-defined domain name. This
    #:  parameter is returned after the domain name is bound.
    bind_access_address = resource.Body("bind_access_address", type=str)
    #: Time when the configuration used by a service is updated,
    #:  in milliseconds calculated from 1970.1.1 0:0:0 UTC
    update_time = resource.Body("update_time", type=float)
    #: Online debugging address of a real-time service.
    #:  This parameter exists only when the model supports online
    #:  debugging and there is only one instance.
    debug_url = resource.Body("debug_url", type=str)
    #: Model ID
    model_id = resource.Body("model_id", type=str)
    #: Model name
    model_name = resource.Body("model_name", type=str)
    #: Model version
    model_version = resource.Body("model_version", type=str)
    #: Model source. This parameter is returned when a model is
    #:  created by an ExeML project. The value is auto.
    source_type = resource.Body("source_type", type=str)
    #: Whether auto scaling is enabled
    scaling = resource.Body("scaling", type=bool)
    #: Whether a model supports online debugging
    support_debug = resource.Body("support_debug", type=str)

    #: Monitoring details, monitor array corresponding to
    #:  infer_type of a service
    monitors = resource.Body("monitors", type=list)
    #: Number of used CPUs
    cpu_core_usage = resource.Body("cpu_core_usage", type=float)
    #: Total number of CPUs
    cpu_core_total = resource.Body("cpu_core_total", type=float)
    #: Used memory, in MBs
    cpu_memory_usage = resource.Body("cpu_memory_usage", type=int)
    #: Total memory, in MBs
    cpu_memory_total = resource.Body("cpu_memory_total", type=int)
    #: Number used GPUs
    gpu_usage = resource.Body("gpu_usage", type=float)
    #: Total number of GPUs
    gpu_total = resource.Body("gpu_total", type=float)

    #: Event logs. For details, see Table 4.
    events = resource.Body("events", type=list, list_type=dict)

    #: Service update logs. For details, see Table 3.
    logs = resource.Body("logs", type=list, list_type=dict)

    #: Node specifications
    specifications = resource.Body("specifications", type=list, list_type=dict)
    tenant = resource.Body("tenant", type=str)
    project = resource.Body("project", type=str)
    owner = resource.Body("owner", type=str)

    publish_at = resource.Body("publish_at", type=float)
    status = resource.Body("status", type=str)

    start_time = resource.Body("start_time", type=float)
    finished_time = resource.Body("finished_time", type=float)
    progress = resource.Body("progress", type=int)
    invocation_times = resource.Body("invocation_times", type=float)
    failed_times = resource.Body("failed_times", type=float)
    is_shared = resource.Body("is_shared", type=bool)
    shared_count = resource.Body("shared_count", type=float)
    schedule = resource.Body("shared_count", type=list)
    due_time = resource.Body("due_time", type=float)
    operation_time = resource.Body("operation_time", type=float)
    is_opened_sample_collection = resource.Body(
        "is_opened_sample_collection", type=str
    )
    transition_at = resource.Body("transition_at", type=float)
    is_free = resource.Body("is_free", type=bool)
    additional_properties = resource.Body("additional_properties", type=dict)

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
