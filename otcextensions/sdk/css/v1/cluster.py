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


STATUS_MAP = {'100': 'CREATING', '200': 'AVAILABLE', '303': 'UNAVAILABLE'}


class FailedReasonSpec(resource.Resource):
    #: Error code.
    error_code = resource.Body('errorCode')
    #: Error details.
    error_msg = resource.Body('errorMsg')


class TagSpec(resource.Resource):
    #: Tag key.
    key = resource.Body('key')
    #: Tag value.
    value = resource.Body('value')


class WhiteListSpec(resource.Resource):
    #: Whether the network access control is enabled.
    is_whitelist_enabled = resource.Body('enableWhiteList', type=bool)
    #: Whitelist for public network access.
    whitelist = resource.Body('whiteList')


class KibanaRespSpec(resource.Resource):
    #: Bandwidth range.
    eip_size = resource.Body('eipSize', type=int)
    #: Kibana public network access information.
    elb_whitelist_resp = resource.Body('elbWhiteListResp', type=WhiteListSpec)
    #: Specifies the IP address for accessing Kibana.
    public_kibana_ip = resource.Body('publicKibanaIp')


class NicsSpec(resource.Resource):
    #: Subnet ID.
    network_id = resource.Body('netId')
    #: Security group ID.
    security_group_id = resource.Body('securityGroupId')
    #: VPC ID, which is used for configuring cluster network.
    router_id = resource.Body('vpcId')


class VolumeSpec(resource.Resource):
    #: Volume size.
    size = resource.Body('size', type=int)
    #: Volume type.
    type = resource.Body('type')
    #: Volume type.
    volume_type = resource.Body('volume_type')


class NodeSpec(resource.Resource):
    #: AZ of a node.
    availability_zone = resource.Body('azCode')
    #: Instance ID.
    id = resource.Body('id')
    #: Instance IP address.
    ip = resource.Body('ip')
    #: Instance name.
    name = resource.Body('name')
    #: Node specifications.
    flavor = resource.Body('specCode')
    #: Node status value.
    status = resource.Body('status')
    #: Type of the current node.
    type = resource.Body('type')
    #: Instance disk information.
    volume = resource.Body('volume', type=VolumeSpec)


class InstanceSpec(resource.Resource):
    #: Availability zone (AZ).
    availability_zone = resource.Body('availability_zone')
    #: Instance flavor name.
    flavor = resource.Body('flavorRef')
    #: Subnet information.
    nics = resource.Body('nics', type=NicsSpec)
    #: Information about the volume.
    volume = resource.Body('volume', type=VolumeSpec)


class DiskEncryptionSpec(resource.Resource):
    #: Key ID.
    system_cmkid = resource.Body('systemCmkid')
    #: Value 1 indicates encryption is performed, and value 0 indicates
    #:  encryption is not performed.
    system_encrypted = resource.Body('systemEncrypted')


class DatastoreSpec(resource.Resource):
    #: Engine type.
    type = resource.Body('type')
    #: Whether security mode is supported.
    version = resource.Body('version')


class BackupStrategySpec(resource.Resource):
    #: IAM agency used to access OBS.
    agency = resource.Body('agency')
    #: Storage path of the snapshot in the OBS bucket.
    base_path = resource.Body('basePath')
    #: OBS bucket used for storing backup.
    bucket = resource.Body('bucket')
    #: Number of days for which automatically created snapshots are reserved.
    keepday = resource.Body('keepday', type=int)
    #: Time when a snapshot is created every day.
    period = resource.Body('period')
    #: Prefix of the name of the snapshot that is automatically created.
    prefix = resource.Body('prefix')


class Cluster(resource.Resource):
    base_path = '/clusters'

    resources_key = 'clusters'
    resource_key = 'cluster'

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True
    allow_fetch = True

    _query_mapping = resource.QueryParameters('start', 'limit')

    # Properties
    #: Cluster behavior progress, which shows the progress of cluster creation
    #:  and scaling in percentage.
    action_progress = resource.Body('actionProgress', type=dict)
    #: Current behavior of a cluster.
    actions = resource.Body('actions', type=list)
    #: Password of the cluster user admin in security mode.
    admin_pwd = resource.Body('adminPwd')
    #: Automatic snapshot creation.
    backup_strategy = resource.Body('backupStrategy', type=BackupStrategySpec)
    #: Public network bandwidth.
    bandwidth_size = resource.Body('bandwidthSize', type=int)
    #: KMS Key ID.
    cmk_id = resource.Body('cmk_id')
    #: Cluster creation time.
    created_at = resource.Body('created')
    #: Type of the data search engine.
    datastore = resource.Body('datastore', type=DatastoreSpec)
    #: Whether disks are encrypted.
    disk_encryption = resource.Body('diskEncryption', type=DiskEncryptionSpec)
    #: Public network access information.
    elb_whitelist = resource.Body('elbWhiteList', type=WhiteListSpec)
    #: IP address and port number of the user used to access the VPC.
    endpoints = resource.Body('endpoint', type=list)
    #: ID of the enterprise project that a cluster belongs to.
    enterprise_project_id = resource.Body('enterpriseProjectId')
    #: Error object
    error = resource.Body('failed_reasons', type=FailedReasonSpec)
    #: Public IP address information.
    floating_ip = resource.Body('publicIp')
    #: Cluster ID.
    id = resource.Body('id')
    #: Instance.
    instance = resource.Body('instance', type=InstanceSpec)
    #: Number of clusters.
    instance_num = resource.Body('instanceNum', type=int)
    #: Whether to enable authentication.
    is_authority_enabled = resource.Body('authorityEnable', type=bool)
    #: Whether cluster is billed.
    is_billed = resource.Body('period')
    #: Whether the snapshot function is enabled.
    is_backup_enabled = resource.Body('backupAvailable', type=bool)
    #: Whether disks are encrypted.
    is_disk_encrypted = resource.Body('diskEncrypted', type=bool)
    #: Communication encryption status.
    is_https_enabled = resource.Body('httpsEnable', type=bool)
    #: Network ID.
    network_id = resource.Body('subnetId')
    #: List of node objects.
    nodes = resource.Body('instances', type=list, list_type=NodeSpec)
    #: Cluster name.
    name = resource.Body('name')
    #: Kibana public network access information.
    public_kibana_resp = resource.Body('publicKibanaResp', type=KibanaRespSpec)
    #: Router (VPC) ID.
    router_id = resource.Body('vpcId')
    #: Security group ID.
    security_group_id = resource.Body('securityGroupId')
    #: Cluster status.
    status = resource.Body('status')
    #: Cluster status code.
    status_code = resource.Body('status_code', type=int)
    #: Cluster tags.
    tags = resource.Body('tags', type=list, list_type=TagSpec)
    #: Last modification time of a cluster.
    updated_at = resource.Body('updated')
    #: Endpoint IP address.
    vpcep_ip = resource.Body('vpcepIp')

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

    def update_flavor(
        self, session, new_flavor, node_type=None, check_replica=True
    ):
        """Modify cluster specifications."""
        body = {
            'newFlavorId': new_flavor
        }
        if check_replica in (True, False):
            body['needCheckReplica'] = check_replica

        url_path = node_type + '/flavor' if node_type else 'flavor'

        self._action(session, url_path, body)

    def update_name(self, session, new_name):
        """Update the name of the CSS cluster."""
        body = {'displayName': new_name}
        self._action(session, 'changename', body)

    def update_password(self, session, new_password):
        """Update the password of the CSS cluster."""
        body = {'newpassword': new_password}
        self._action(session, 'password/reset', body)

    def update_security_mode(
        self,
        session,
        https_enable=None,
        authority_enable=None,
        admin_pwd=None,
    ):
        body = {}
        if https_enable in (True, False):
            body['httpsEnable'] = https_enable
        if authority_enable in (True, False):
            body['authorityEnable'] = authority_enable
        if admin_pwd:
            body['adminPwd'] = admin_pwd

        self._action(session, 'mode/change', body)

    def update_security_group(self, session, security_group_id):
        """Update security group of the CSS cluster."""
        body = {'security_group_ids': security_group_id}
        self._action(session, 'sg/change', body)

    def update_kernel(
        self,
        session,
        target_image_id,
        upgrade_type,
        indices_backup_check,
        agency,
        cluster_load_check=True,
    ):
        """Update the kernel of the CSS cluster."""
        body = {
            'target_image_id': target_image_id,
            'upgrade_type': upgrade_type,
            'indices_backup_check': indices_backup_check,
            'agency': agency,
        }
        if cluster_load_check in (True, False):
            body['cluster_load_check'] = cluster_load_check

        self._action(session, 'inst-type/all/image/upgrade', body)

    def scale_in(self, session, nodes):
        """Scale in a cluster by removing specified nodes."""
        if not isinstance(nodes, list):
            raise exceptions.SDKException(
                'nodes parameter should be list type'
            )

        body = {'shrinkNodes': nodes}

        self._action(session, 'node/offline', body)

    def scale_in_by_node_type(self, session, nodes):
        """Remove instances of specific types and reduce instance
        storage capacity in a cluster."""
        if not isinstance(nodes, list):
            raise exceptions.SDKException(
                'nodes parameter should be list of dictionary items'
            )

        data = []

        for item in nodes:
            node_type = item.get('type')
            reduced_node_num = item.get('reducedNodeNum')
            if node_type not in (
                'ess',
                'ess-master',
                'ess-client',
                'ess-cold',
            ):
                raise ValueError(
                    f'Unsupported node type: {node_type}. Supported '
                    'node_type can be ess, ess-master, ess-client, ess-cold,'
                )
            if not isinstance(reduced_node_num, int) or reduced_node_num < 1:
                raise ValueError(
                    f'Reduced node number for {node_type} must be '
                    'a non-negative integer.'
                )

            data.append(
                {
                    'type': node_type.replace('_', '-'),
                    'reducedNodeNum': reduced_node_num,
                }
            )
        endpoint = session.get_endpoint().replace("v1.0", "v1.0/extend")

        url = utils.urljoin(endpoint, 'clusters', self.id, 'role/shrink')
        response = session.post(url, json={'shrink': data})
        exceptions.raise_from_response(response)

    def replace_node(self, session, node_id):
        """Replacing cluster node."""
        uri = utils.urljoin(
            'clusters', self.id, 'instance', node_id, 'replace'
        )
        response = session.put(uri)
        exceptions.raise_from_response(response)

    def add_nodes(self, session, node_type, flavor, node_size, volume_type):
        """Adding master and client node to cluster."""

        body = {
            'type': {
                'flavor_ref': flavor,
                'node_size': node_size,
                'volume_type': volume_type,
            }
        }

        self._action(session, f'type/{node_type}/independent', body)

    def retry_upgrade_job(self, session, job_id, retry_mode=None):
        """Retry a task or terminate the impact of a task."""
        uri = utils.urljoin('clusters', self.id, 'upgrade', job_id, 'retry')

        params = {}

        if retry_mode:
            params['retry_mode'] = 'abort'

        response = session.put(uri, params=params)
        exceptions.raise_from_response(response)

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
        if 'status' in kwargs.keys():
            kwargs['status_code'] = kwargs['status']
            kwargs['status'] = STATUS_MAP.get(str(kwargs['status']), 'ERROR')
        if kwargs.get('endpoint'):
            kwargs['endpoint'] = kwargs['endpoint'].split(',')
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
                body.pop('self', None)

                if 'status' in body.keys():
                    body['status_code'] = body['status']
                    body['status'] = STATUS_MAP.get(
                        str(body['status']), 'ERROR'
                    )
                if body.get('endpoint'):
                    body['endpoint'] = body['endpoint'].split(',')
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
