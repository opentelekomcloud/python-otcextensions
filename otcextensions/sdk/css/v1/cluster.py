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
from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.common import format as otc_format


class DatastoreSpec(resource.Resource):
    #: Datastore version
    version = resource.Body('version', default='6.2.3')
    #: Engine type
    type = resource.Body('type', default='elasticsearch')


class NetworkSpec(resource.Resource):
    #: Router ID (VPC id)
    router_id = resource.Body('vpcId')
    #: Network ID
    network_id = resource.Body('netId')
    #: Security group ID
    security_group_id = resource.Body('securityGroupId')


class InstanceSpec(resource.Resource):
    #: Instance flavor name
    flavor = resource.Body('flavorRef')
    #: Volume object {volume_type:[COMMON, HIGH, ULTRAHIGH], size:int}
    volume = resource.Body('volume', type=dict)
    #: Network information
    nics = resource.Body('nics', type=NetworkSpec)
    #: Availability zone
    availability_zone = resource.Body('availability_zone')


class DiskEncryption(resource.Resource):
    #: Disk encryption flag
    is_disk_encrypted = resource.Body('systemEncrypted',
                                      type=otc_format.Bool_10)
    #: KMS Key ID
    cms_id = resource.Body('systemCmkid')


class BackupStrategy(resource.Resource):
    #: Time when a snapshot is created every day.
    period = resource.Body('period')
    #: Prefix of the name of the snapshot that is automatically created.
    prefix = resource.Body('prefix')
    #: Number of days for which automatically created snapshots are reserved.
    keepday = resource.Body('keepday')
    #: OBS bucket used for storing backup.
    bucket = resource.Body('bucket')
    #: Storage path of the snapshot in the OBS bucket.
    basepath = resource.Body('basePath')
    #: IAM agency used to access OBS.
    agency = resource.Body('agency')


class Cluster(resource.Resource):
    base_path = '/clusters'

    resources_key = 'clusters'
    resource_key = 'cluster'

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    _query_mapping = resource.QueryParameters(
        'id', 'start', 'limit')

    # Properties
    #: Current actions
    actions = resource.Body('actions', type=list)
    #: KMS Key ID (read only)
    cmk_id = resource.Body('cmkId')
    #: Cluster creation time
    created_at = resource.Body('created')
    #: Type of the data search engine
    datastore = resource.Body('datastore', type=DatastoreSpec)
    #: Disk encryption specification
    disk_encryption = resource.Body('diskEncryption', type=DiskEncryption)
    #: Error object
    error = resource.Body('failed_reasons', type=dict)
    #: Cluster endpoint
    endpoint = resource.Body('endpoint')
    #: Instance object
    instance = resource.Body('instance', type=InstanceSpec)
    #: Cluster nodes (read only)
    nodes = resource.Body('instances', type=list, list_type=dict)
    #: Number of cluster instances (1..32)
    instance_count = resource.Body('instanceNum', type=int)
    #: Disk encryption flag (read only)
    is_disk_encrypted = resource.Body('diskEncrypted', type=bool)
    #: Whether communication encyption is performed on the cluster
    is_https_enabled = resource.Body('httpsEnable', type=otc_format.BoolStr_1)
    #: Operation progress
    progress = resource.Body('actionProgress', type=dict)
    #: Router ID (read only)
    router_id = resource.Body('vpcId')
    #: Security group ID (read only)
    security_group_id = resource.Body('securityGroupId')
    #: Cluster status:
    #:  - 100: Cluster is being created
    #:  - 200: Available
    #:  - 300: Unavailable
    status = resource.Body('status')
    #: Subnetwork ID (read only)
    subnet_id = resource.Body('subnetId')
    #: Cluster update time
    updated_at = resource.Body('updated')
    #: Restart Cluster Job ID
    jobId = resource.Body('jobId')
    #: Array of tags
    tags = resource.Body('tags', type=list)
    #: Automatic snapshot creation
    backup_strategy = resource.Body('backupStrategy', type=BackupStrategy)

    def _action(self, session, action, body=None):
        """Preform actions given the message body.
        """
        url = utils.urljoin(self.base_path, self.id, action)
        return session.post(url, json=body)

    def restart(self, session):
        """Restart the cluster.
        """
        res = self._action(session, 'restart')
        self._translate_response(res)
        return self

    def extend(self, session, add_nodes):
        """Extend cluster capacity.
        """
        if not 0 < add_nodes <= 32:
            raise exceptions.SDKException('CSS Cluster size can be [1..32]')
        res = self._action(session, 'extend',
                           {'grow': {'modifySize': add_nodes}})
        self._translate_response(res)
        return self

    @classmethod
    def list(cls, session, paginated=False, base_path=None,
             allow_unknown_params=False, **params):

        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion(session, action='list')

        if base_path is None:
            base_path = cls.base_path
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=allow_unknown_params)

        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        limit = query_params.get('limit')

        # Track the total number of resources yielded so we can paginate
        # swift objects
        total_yielded = query_params.get('start', 0)
        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion)
            exceptions.raise_from_response(response)
            data = response.json()

            # Discard any existing pagination keys
            query_params.pop('start', None)
            query_params.pop('limit', None)

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            marker = None
            for raw_resource in resources:
                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource)
                marker = total_yielded + 1
                yield value
                total_yielded += 1

            if resources and paginated:
                uri, next_params = cls._get_next_link(
                    uri, response, data, marker, limit, total_yielded)
                query_params.update(next_params)
            else:
                return
