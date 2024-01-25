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
    #: Additional service attribute.
    additional_properties = resource.Body("additional_properties", type=dict)
    #: Access address of an inference request. This parameter is
    #:  returned when infer_type is set to real-time.
    access_address = resource.Body("access_address")
    #: Request address of the user-defined domain name. This
    #:  parameter is returned after the domain name is bound.
    bind_access_address = resource.Body("bind_access_address", type=str)
    #: ID of a dedicated cluster. This parameter is left blank by default,
    #:  indicating that no dedicated cluster is used.
    cluster_id = resource.Body("cluster_id")
    #: Model running configuration. If infer_type is batch,
    #:  you can configure only one model.
    config = resource.Body("config", type=list, list_type=dict)
    #: Online debugging address of a real-time service.
    #:  This parameter exists only when the model supports online
    #:  debugging and there is only one instance.
    debug_url = resource.Body("debug_url", type=str)
    #: Service description, which contains a maximum of 100 characters.
    #:  By default, this parameter is left blank.
    description = resource.Body("description", type=str)
    #: Time when a real-time service automatically stops,
    #:  in milliseconds calculated from 1970.1.1 0:0:0 UTC.
    due_time = resource.Body("due_time", type=int)
    #: Error message. When status is failed, an error message
    #:  carrying the failure cause is returned.
    error_msg = resource.Body("error_msg")
    #: Number of failed service calls.
    failed_times = resource.Body("failed_times", type=int)
    #: Inference mode. The value can be real-time, batch.
    #:  real-time: real-time service. The service keeps running.
    #:  batch: batch service, which can be configured as tasks to run in
    #:  batches. When the tasks are completed, the service stops
    #:  automatically.
    infer_type = resource.Body("infer_type")
    #: Total number of service calls.
    invocation_times = resource.Body("invocation_times", type=int)
    #: Whether a free-of-charge flavor is used.
    is_free = resource.Body("is_free", type=bool)
    #: Whether a service is subscribed.
    is_shared = resource.Body("is_shared", type=bool)
    #: Network ID.
    network_id = resource.Body("subnet_network_id")
    #: Operation time of a request.
    operation_time = resource.Body("operation_time", type=int)
    #: Owner ID.
    owner = resource.Body("owner")
    #: Deployment progress. This parameter is available
    #:  when the status is deploying.
    progress = resource.Body("progress", type=int)
    #: Project ID.
    project = resource.Body("project")
    #: Latest service release time, in milliseconds.
    publish_at = resource.Body("publish_at", type=int)
    #: ID of the VPC to which a real-time service instance is deployed.
    router_id = resource.Body("vpc_id")
    #: Service scheduling configuration, which can be configured only
    #:  for real-time services. By default, this parameter is not used.
    schedule = resource.Body("schedule", type=list, list_type=dict)
    #: Security group. By default, this parameter is left blank.
    #:  This parameter is mandatory when router_id is configured.
    security_group_id = resource.Body("security_group_id")
    #: Service ID.
    service_id = resource.Body("service_id", alternate_id=True)
    #: Service name. The value can contain 1 to 64 visible characters,
    #:  including Chinese characters.
    service_name = resource.Body("service_name")
    #: Number of subscribed services.
    shared_count = resource.Body("shared_count", type=int)
    #: Service status, which can be running, deploying,
    #:  concerning, failed, stopped, or finished.
    status = resource.Body("status", type=str)
    #: Tenant ID.
    tenant = resource.Body("tenant")
    #: Time when the service status changes.
    transition_at = resource.Body("transition_at", type=int)
    #: Time when the configuration used by a service is updated,
    #:  in milliseconds calculated from 1970.1.1 0:0:0 UTC
    update_time = resource.Body("update_time", type=int)
    #: ID of the workspace to which a service belongs.
    #:  The default value is 0, indicating the default workspace.
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
