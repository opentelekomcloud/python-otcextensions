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
from openstack import exceptions
from openstack import resource
from openstack import utils
from otcextensions.sdk.modelartsv1.v1 import _base


class Spec(resource.Resource):
    class AutoStop(resource.Resource):
        #: Whether auto stop function is enabled.
        is_enabled = resource.Body("enable", type=bool)
        #: Running duration, in seconds.
        duration = resource.Body("duration", type=int)
        #: Whether to display a prompt again. This parameter
        #:  is provided for the console to use.
        is_prompted = resource.Body("prompt", type=bool)
        #: Time when the instance stops. The value is a 13-digit timestamp.
        stop_timestamp = resource.Body("stop_timestamp", type=int)
        #: Remaining time before actual stop, in seconds
        remaining_time = resource.Body("remain_time", type=int)

    #: Annotations.
    annotations = resource.Body("annotations", type=dict)
    #: Auto stop parameter.
    auto_stop = resource.Body("auto_stop", type=AutoStop)
    #: Path for storing custom initialization scripts used
    #:  when a notebook instance is started.
    custom_script_path = resource.Body("custom_script_path")
    #: Extended parameters.
    extended_params = resource.Body("extend_params", type=dict)
    #: Extend Storage.
    extend_storage = resource.Body("extend_storage")
    #: Cause for a creation or startup failure.
    failed_reasons = resource.Body("failed_reasons", type=dict)
    #: Path for storing custom image logs.
    log_path = resource.Body("log_path")
    #: Git repository information.
    repository = resource.Body("repository", type=dict)
    #: Time when the resource is reserved.
    resource_reserved_timestamp = resource.Body(
        "resource_reserved_timestamp", type=int
    )
    #: Storage path.
    storage = resource.Body("storage", type=dict)


class Profile(resource.Resource):
    class Provision(resource.Resource):
        class Spec(resource.Resource):
            class Params(resource.Resource):
                #: SWR organization name, which is globally unique.
                namespace = resource.Body("namespace")
                #: Image name.
                image_name = resource.Body("image_name")
                #: Image tag.
                image_tag = resource.Body("image_tag")
                #: Label information, which can be extended.
                annotations = resource.Body("annotations", type=dict)

            #: Deployment engine. Only CCE is supported.
            engine = resource.Body("engine")
            #: Deployment parameters. Only Docker is supported.
            params = resource.Body("params", type=Params)

        #: Deployment type. Only Docker is supported.
        type = resource.Body("type")
        #: Deployment details.
        spec = resource.Body("spec", type=Spec)

    #: Development environment type. Currently, only notebook is supported.
    de_type = resource.Body("de_type")
    #: Configuration description.
    description = resource.Body("description")
    #: Hardware, including CPU, GPU, and Ascend
    flavor_type = resource.Body("flavor_type")
    #: Deployment information.
    provision = resource.Body("provision", type=Provision)
    #: Label information.
    labels = resource.Body("labels", type=dict)


class Devenv(_base.Resource):
    base_path = "/demanager/instances"

    resources_key = "instances"
    # resource_key = '' #'instances'

    _query_mapping = resource.QueryParameters(
        "de_type",
        "provision_type",
        "status",
        "sortby",
        "order",
        "workspace_id",
        "pool_id",
        "ai_project",
        "limit",
        "offset",
        "show_self",
        ai_project="ai_project_id",
    )

    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    # Properties
    #: AI project.
    ai_project = resource.Body("ai_project", type=dict)
    #: AI project ID.
    ai_project_id = resource.Body("ai_project_id")
    #: Time when an instance is created.
    created_at = resource.Body("creation_timestamp", type=str)
    #: Current status of an instance.
    current_status = resource.Body("current_status", type=str)
    #: Instance description.
    description = resource.Body("description", type=str)
    #: Error code.
    error_code = resource.Body("error_code", type=str)
    #: Instance flavor.
    flavor = resource.Body("flavor", type=str)
    #: Details about the flavor.
    flavor_details = resource.Body("flavor_details", type=dict)
    #: Instance ID.
    instance_id = resource.Body("instance_id", type=str)
    #: Details about the dedicated resource pool.
    pool = resource.Body("pool", type=dict)
    #: Previous status of an instance.
    previous_state = resource.Body("previous_state")
    #: Configuration ID.
    profile_id = resource.Body("profile_id")
    #: Configuration information.
    profile = resource.Body("profile", type=dict)
    #: Queuing information.
    queuing_info = resource.Body("queuing_info")
    #: Git repository information.
    repository = resource.Body("repository")
    #:  Instance definition.
    spec = resource.Body("spec", type=dict)
    #: Instance status.
    status = resource.Body("status", type=str)
    #: Latest Update Timestamp.
    updated_at = resource.Body("latest_update_timestamp", type=str)
    #: User information.
    user = resource.Body("user", type=dict)
    #: Workspace.
    workspace = resource.Body("workspace", type=dict)
    #: Workspace ID.
    workspace_id = resource.Body("workspace_id")

    def _action(self, session, action):
        """Preform actions given the message body."""
        url = utils.urljoin(self.base_path, self.id, "action")
        body = {"action": action}
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }
        response = session.post(url, json=body, headers=headers)
        self._translate_response(response)
        return self

    def start(self, session):
        """start the DevEnv Instance."""
        return self._action(session, "start")

    def stop(self, session):
        """stop the DevEnv Instance."""
        return self._action(session, "stop")

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
            body = response.json()
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

            if body.get("workspace") and body["workspace"].get("id"):
                body["workspace_id"] = body["workspace"]["id"]

            if body.get("ai_project") and body["ai_project"].get("id"):
                body["ai_project_id"] = body["ai_project"]["id"]

            body = self._consume_body_attrs(body)
            self._body.attributes.update(body)
            self._body.clean()
            if self.commit_jsonpatch:
                # We need the original body to compare against
                self._original_body = body.copy()

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
