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


class CredentialSpec(resource.Resource):
    #: OAuth token of GitHub.
    access_token = resource.Body("access_token")
    #: SSH private certificate.
    ssh_private_key = resource.Body("ssh_private_key")


class ConnectionInfoSpec(resource.Resource):
    #: Certificate information.
    credential = resource.Body("credential", type=CredentialSpec)
    #: Repository link protocol.
    protocol = resource.Body("protocol")
    #: Repository link address.
    url = resource.Body("url")


class RepositorySpec(resource.Resource):
    #: Repository branch.
    branch = resource.Body("branch")
    #: Repository link information.
    connection_info = resource.Body("connection_info", type=ConnectionInfoSpec)
    #: Repository ID.
    id = resource.Body("id")
    #: Repository type.
    type = resource.Body("type")
    #: Repository user mailbox.
    user_email = resource.Body("user_email")
    #: Repository username.
    user_name = resource.Body("user_name")


class AutoStopSpec(resource.Resource):
    #: Running duration, in seconds.
    duration = resource.Body("duration", type=int)
    #: Whether to enable the auto stop function.
    enable = resource.Body("enable", type=bool)
    #: Whether to display a prompt again.
    prompt = resource.Body("prompt", type=bool)
    #: Remaining time before actual stop, in seconds.
    remain_time = resource.Body("remain_time", type=int)
    #: Time when the instance stops.
    stop_timestamp = resource.Body("stop_timestamp", type=int)


class FailedReasonsSpec(resource.Resource):
    #: Error code.
    code = resource.Body("code")
    #: Error details.
    detail = resource.Body("detail", type=dict)
    #: Error message.
    message = resource.Body("message")


class LocationSpec(resource.Resource):
    #: Storage pathIf type is set to obs, this parameter is mandatory.
    path = resource.Body("path")
    #: If type is set to obs, this parameter does not need to be set.
    volume_size = resource.Body("volume_size", type=int)
    #: Volume stotage unit.
    volume_unit = resource.Body("volume_unit")


class StorageSpec(resource.Resource):
    #: Storage location.
    location = resource.Body("location", type=LocationSpec)
    #: Storage type.
    type = resource.Body("type")


class NotebookSpec(resource.Resource):
    #: AnnotationsThe generated URL cannot be directly accessed.
    annotations = resource.Body("annotations", type=dict)
    #: Auto stop parameter.
    auto_stop = resource.Body("auto_stop", type=AutoStopSpec)
    #: AK and SK for accessing OBS.
    credential = resource.Body("credential", type=CredentialSpec)
    #: Path for storing custom initialization scripts used when a notebook
    #:  instance is started.
    custom_script_path = resource.Body("custom_script_path")
    #: Extended parameter.
    extend_params = resource.Body("extend_params", type=dict)
    #: Extended storage list.
    extend_storage = resource.Body(
        "extend_storage", type=list, list_type=StorageSpec
    )
    #: Cause for a creation or startup failure.
    failed_reasons = resource.Body("failed_reasons", type=FailedReasonsSpec)
    #: Path for storing custom image logs.
    log_path = resource.Body("log_path")
    #: Git repository information.
    repository = resource.Body("repository", type=RepositorySpec)
    #: Time when the resource is reserved.
    resource_reserved_timestamp = resource.Body(
        "resource_reserved_timestamp", type=int
    )
    #: Storage path.
    storage = resource.Body("storage", type=StorageSpec)


class PoolSpec(resource.Resource):
    #: ID of a resource pool.
    id = resource.Body("id")
    #: Name of a resource pool.
    name = resource.Body("name")
    #: This parameter is mandatory when type is set to USER_DEFINED.
    owner = resource.Body("owner", type=dict)
    #: Type of a resource pool.
    type = resource.Body("type")


class FlavorDetailsSpec(resource.Resource):
    #: Billing specifications.
    billing_flavor = resource.Body("billing_flavor")
    #: Billing ratio This parameter is mandatory when billing_flavor is
    #:  specified.
    billing_params = resource.Body("billing_params", type=int)
    #: Auto stop time after startup, in seconds.
    duration = resource.Body("duration", type=int)
    #: Number of instances of this flavor the current created.
    instance_num = resource.Body("instance_num", type=int)
    #: Whether the current user has the permission to use this flavor.
    is_permitted = resource.Body("is_permitted", type=bool)
    #: Flavor name.
    name = resource.Body("name")
    #: Parameters that describing flavor.
    params = resource.Body("params", type=dict)
    #: Parameters that describing flavor.
    params_extends = resource.Body("params_extends", type=dict)
    #: Promotion type.
    promo_type = resource.Body("promo_type")
    #: Left queuing time, in secondsThis parameter is mandatory when
    #:  promo_type is set to Free and status is set to soldOut.
    queue_left_time = resource.Body("queue_left_time", type=int)
    #: This parameter is mandatory when promo_type is set to Free and status
    #:  is set to soldOut.
    queuing_num = resource.Body("queuing_num", type=int)
    #: Flavor sale status The options are as follows:onSalesoldOut.
    status = resource.Body("status")
    #: Supported storage type.
    storage_list = resource.Body("storage_list", type=list)
    #: Maximum retention period of an inactive instance of this flavor in the
    #:  database, in hoursThe default value is -1, indicating that the instance
    #:  can be permanently saved.
    store_time = resource.Body("store_time", type=int)
    #: Flavor status.
    type = resource.Body("type")


class QueuingInfoSpec(resource.Resource):
    #: Time when an instance starts queuing.
    begin_timestamp = resource.Body("begin_timestamp", type=int)
    #: Development environment type.
    dev_env_type = resource.Body("de_type")
    #: Time when an instance completes queuing.
    end_timestamp = resource.Body("end_timestamp", type=int)
    #: Instance flavor.
    flavor = resource.Body("flavor")
    #: Flavor details, which display the flavor information and whether the
    #:  flavor is sold out.
    flavor_details = resource.Body("flavor_details", type=FlavorDetailsSpec)
    #: Instance ID.
    id = resource.Body("id")
    #: Instance name.
    name = resource.Body("name")
    #: Ranking of an instance in a queue.
    rank = resource.Body("rank", type=int)
    #: Left queuing time, in seconds.
    remain_time = resource.Body("remain_time", type=int)
    #: Instance status.
    status = resource.Body("status")


class DockerSpec(resource.Resource):
    #: Label information, which can be extended.
    annotations = resource.Body("annotations", type=dict)
    #: Image name.
    image_name = resource.Body("image_name")
    #: Image tag.
    image_tag = resource.Body("image_tag")
    #: SWR organization name, which is globally unique.
    namespace = resource.Body("namespace")


class ProvisionSpecSpec(resource.Resource):
    #: Deployment engine.
    engine = resource.Body("engine")
    #: Deployment parameters.
    params = resource.Body("params", type=DockerSpec)


class ProvisionSpec(resource.Resource):
    #: Provision annotations.
    annotations = resource.Body("annotations", type=dict)
    #: Deployment details.
    spec = resource.Body("spec", type=ProvisionSpecSpec)
    #: Deployment type.
    type = resource.Body("type")


class ProfileSpec(resource.Resource):
    #: Development environment type.
    dev_env_type = resource.Body("de_type")
    #: Configuration description.
    description = resource.Body("description")
    #: Hardware, which can be CPU, GPU.
    flavor_type = resource.Body("flavor_type")
    #: Configuration ID.
    id = resource.Body("id")
    #: Label.
    labels = resource.Body("labels", type=dict)
    #: Configuration name.
    name = resource.Body("name")
    #: Deployment information.
    provision = resource.Body("provision", type=ProvisionSpec)


class Devenv(resource.Resource):
    base_path = "/demanager/instances"

    resources_key = "instances"

    _query_mapping = resource.QueryParameters(
        "ai_project",
        "dev_env_type",
        "limit",
        "order",
        "pool_id",
        "provision_type",
        "offset",
        "show_self",
        "sort_by",
        "status",
        "workspace_id",
        dev_env_type="de_type",
        ai_project="ai_project_id",
        sort_by="sortby",
    )

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    # Properties

    #: AI project.
    ai_project = resource.Body("ai_project", type=dict)
    #: AI project ID.
    ai_project_id = resource.Body("ai_project_id")
    #: Auto stop parameters.
    auto_stop = resource.Body("auto_stop", type=dict)
    #: Time when an instance is created.
    created_at = resource.Body("creation_timestamp")
    #: Current status of an instance.
    current_status = resource.Body("current_status", type=str)
    #: Instance description.
    description = resource.Body("description")
    #: Error code.
    error_code = resource.Body("error_code")
    #: Instance flavor.
    flavor = resource.Body("flavor")
    #: For details about the flavor, see Table 16.
    flavor_details = resource.Body("flavor_details", type=FlavorDetailsSpec)
    #: Instance ID.
    id = resource.Body("id")
    #: Instance name.
    name = resource.Body("name")
    #: For details about the dedicated resource pool, see Table 17.
    pool = resource.Body("pool", type=PoolSpec)
    #: Previous status of an instance.
    previous_state = resource.Body("previous_state")
    #: Configuration information.
    profile = resource.Body("profile", type=ProfileSpec)
    #: Configuration ID.
    profile_id = resource.Body("profile_id")
    #: Queuing information.
    queuing_info = resource.Body("queuing_info", type=QueuingInfoSpec)
    #: Git repository information.
    repository = resource.Body("repository", type=RepositorySpec)
    #: Instance definition For details about parameters of a notebook
    #:  instance, see Table 19.
    spec = resource.Body("spec", type=NotebookSpec)
    #: Instance status.
    status = resource.Body("status")
    #: Latest Update Timestamp.
    updated_at = resource.Body("latest_update_timestamp", type=str)
    #: User information.
    user = resource.Body("user", type=dict)
    #: Workspace.
    workspace = resource.Body("workspace", type=dict)
    #: Workspace ID.
    workspace_id = resource.Body("workspace_id")

    def _action(self, session, action):
        """Perform actions given the message body."""
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

    def _translate_response(self, response, has_body=None, error_message=None,
                            resource_response_key=None):
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
