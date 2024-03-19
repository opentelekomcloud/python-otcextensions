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

STATUS_MAP = {"100": "CREATING", "200": "AVAILABLE", "303": "UNAVAILABLE"}


class NodeSpec(resource.Resource):
    #: Availability Zone.
    availability_zone = resource.Body('azCode')
    #: Node flavor
    flavor = resource.Body('specCode')
    #: CSS Node Type.
    node_type = resource.Body('type')
    #: Private IP of Cluster Node.
    private_ip = resource.Body('ip')
    #: Cluster Node Status
    status = resource.Body('status')
    #: Volume object {volume_type:[COMMON, HIGH, ULTRAHIGH], size:int}
    volume = resource.Body('volume', type=dict)


class Cluster(resource.Resource):
    base_path = '/clusters'

    resources_key = 'clusters'
    resource_key = 'cluster'

    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters('id', 'start', 'limit')

    # Properties
    #: Current actions
    actions = resource.Body('actions', type=list)
    #: Operation progress
    action_progress = resource.Body('actionProgress', type=dict)
    #: Password of the cluster user admin in security mode. This parameter
    #:  is mandatory only when authorityEnable is set to true.
    admin_password = resource.Body('adminPwd')
    #: Automatic snapshot creation.
    backup_strategy = resource.Body('backupStrategy', type=dict)
    #: Bandwidth of Public IP
    bandwidth_size = resource.Body('bandwidthSize')
    #: KMS Key ID.
    cmk_id = resource.Body('cmk_id')
    #: Cluster creation time
    created_at = resource.Body('created')
    #: Type of the data search engine
    datastore = resource.Body('datastore', type=dict)
    #: Disk Encryption Object. (For request body only)
    disk_encryption = resource.Body('diskEncryption', type=dict)
    #: Elb Whitelist Details
    elb_whitelist = resource.Body('elbWhiteList', type=dict)
    #: Indicates the IP address and port number of the user used to
    #:  access the VPC.
    endpoint = resource.Body('endpoint')
    #: Error object
    error = resource.Body('failed_reasons', type=dict)
    #: Public IP address.
    floating_ip = resource.Body('publicIp')
    #: Cluster Node (request Body)
    instance = resource.Body('instance', type=dict)
    #: Number of cluster Nodes. The value range is 1 to 32. (request Body)
    instance_num = resource.Body('instanceNum', type=int)
    #: Whether authentication is enabled.
    #:  When authentication is enabled, httpsEnable must be set to true.
    is_authority_enabled = resource.Body('authorityEnable', type=bool)
    #: Whether the cluster is billed.
    is_billed = resource.Body('period', type=bool)
    #: Whether backup is enabled.
    is_backup_enabled = resource.Body('backupAvailable', type=bool)
    #: Whether Disk is Encrypted
    is_disk_encrypted = resource.Body('diskEncrypted', type=bool)
    #: Communication encryption status.
    is_https_enabled = resource.Body('httpsEnable', type=bool)
    #: ID of the restart task.
    job_id = resource.Body('jobId')
    #: Network ID.
    network_id = resource.Body('subnetId')
    #: Cluster nodes. List of node objects.
    nodes = resource.Body('instances', type=list, list_type=NodeSpec)
    #: Public Kibana Response.
    public_kibana_resp = resource.Body('publicKibanaResp')
    #: Router ID.
    router_id = resource.Body('vpcId')
    #: Security group ID (read only)
    security_group_id = resource.Body('securityGroupId')
    #: Return value.
    #:  100: The operation, such as instance creation, is in progress.
    #:  200: The cluster is available.
    #:  303: The cluster is unavailable.
    status_code = resource.Body('status', type=int)
    #: Cluster Status.
    status = resource.Body('status')
    #: Array of tags
    tags = resource.Body('tags', type=list, list_type=dict)
    #: Cluster update time
    updated_at = resource.Body('updated')

    # Computed Properties
    #: Number of Nodes.
    num_nodes = resource.Computed('num_nodes', type=int)

    def _action(self, session, action, body=None):
        """Preform actions given the message body."""
        uri = utils.urljoin('clusters', self.id, action)
        response = session.post(uri, json=body)
        exceptions.raise_from_response(response)

    def restart(self, session):
        """Restart the cluster."""
        self._action(session, 'restart')

    def extend(self, session, add_nodes):
        """Scaling Out a Cluster with only Common Nodes."""
        if not 0 < add_nodes <= 32:
            raise exceptions.SDKException('CSS Cluster size can be [1..32]')
        self._action(session, 'extend', {'grow': {'modifySize': add_nodes}})

    @classmethod
    def existing(cls, connection=None, **kwargs):
        """Create an instance of an existing remote resource.

        When creating the instance set the ``_synchronized`` parameter
        of :class:`Resource` to ``True`` to indicate that it represents the
        state of an existing server-side resource. As such, all attributes
        passed in ``**kwargs`` are considered "clean", such that an immediate
        :meth:`update` call would not generate a body of attributes to be
        modified on the server.

        :param dict kwargs: Each of the named arguments will be set as
            attributes on the resulting Resource object.
        """
        if "status" in kwargs.keys():
            kwargs["status"] = STATUS_MAP.get(str(kwargs["status"]), "ERROR")
        return cls(_synchronized=True, connection=connection, **kwargs)

    def _translate_response(
        self,
        response,
        has_body=None,
        error_message=None,
        *,
        resource_response_key=None,
    ):
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
                if resource_response_key and resource_response_key in body:
                    body = body[resource_response_key]
                elif self.resource_key and self.resource_key in body:
                    body = body[self.resource_key]

                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                body.pop("self", None)

                if "status" in body.keys():
                    body["status"] = STATUS_MAP.get(
                        str(body["status"]), "ERROR"
                    )

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


class ExtendClusterNodes(resource.Resource):
    base_path = '/clusters/%(cluster_id)s/role_extend'

    allow_create = True

    cluster_id = resource.URI('cluster_id')

    # Properties
    #: Detailed description about the cluster scale-out request.
    grow = resource.Body('grow', type=list, list_type=dict)
