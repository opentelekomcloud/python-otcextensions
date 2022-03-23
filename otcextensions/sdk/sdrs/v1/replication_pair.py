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
from openstack import resource
from openstack import utils
from openstack import exceptions


class Attachment(resource.Resource):
    #: Properties
    #: Protected instance attached disk name
    device = resource.Body('device')
    #: Protected instance ID
    protected_instance = resource.Body('protected_instance')


class Metadata(resource.Resource):
    #: Properties
    #: Specifies whether disk is system
    bootable = resource.Body('bootable', type=bool)
    #: Specifies whether disk is shared
    multiattach = resource.Body('multiattach', type=bool)
    #: Replication pair disk size
    volume_size = resource.Body('volume_size', type=int)
    #: Replication pair disk type
    volume_type = resource.Body('volume_type')


class ReplicationPair(resource.Resource):
    """SDRS Replication pair Resource"""
    resource_key = 'replication'
    resources_key = 'replications'
    base_path = '/replications'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'availability_zone', 'limit', 'marker', 'name', 'offset',
        'protected_instance_id', 'protected_instance_ids', 'query_type',
        'server_group_id', 'server_group_ids', 'status')

    #: Properties
    #: Attached replication pair info
    attachment = resource.Body('attachment', type=list, list_type=Attachment)
    #: Creation time
    created_at = resource.Body('created_at')
    #: Option to delete DR site disk
    delete_target_volume = resource.Body('delete_target_volume',
                                         type=bool)
    #: Replication pair description
    description = resource.Body('description')
    #: Replication pair error code
    failure_detail = resource.Body('failure_detail')
    #: Replication pair fault level
    fault_level = resource.Body('fault_level')
    #: Job id for created task
    job_id = resource.Body('job_id')
    #: Replication pair ID
    id = resource.Body('id')
    #: Replication pair name
    name = resource.Body('name')
    #: Production site AZ of the protection group
    #: containing the replication pair
    priority_station = resource.Body('priority_station')
    #: Replication pair synchronization progress
    progress = resource.Body('progress', type=int)
    #: Replication pair SDR data
    record_metadata = resource.Body('record_metadata', type=Metadata)
    #: Replication pair mode
    #: Default: 'hypermetro'
    replication_model = resource.Body('replication_model')
    #: Synchronization status
    replication_status = resource.Body('replication_status')
    #: Protection group ID
    server_group_id = resource.Body('server_group_id')
    #: Replication pair status
    status = resource.Body('status')
    #: Update time
    updated_at = resource.Body('updated_at')
    #: Production site volume ID
    volume_id = resource.Body('volume_id')
    #: Production and DR site disk IDs
    volume_ids = resource.Body('volume_ids')

    def delete(self, session,
               server_group_id=None, delete_target_volume=False,
               ignore_missing=True):
        """Delete the remote resource based on this instance.

        This function overrides default Resource.delete to enable params

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param bool server_group_id: Specifies the ID of protection
            group
        :param bool delete_target_volume: Specifies whether DR site
            EVS disk should be deleted after replication pair deletion
        :param bool ignore_missing: When set to ``False``
            :class:`~openstack.exceptions.ResourceNotFound` will be raised
            when the replication pair does not exist.
            When set to ``True``, no exception will be set when attempting
            to delete a nonexistent replication pair
        :return: This :class:`Replication` instance.
        """
        body = {
            'replication': {
                'delete_target_volume': delete_target_volume
            }
        }
        if server_group_id:
            body['replication']['server_group_id'] = server_group_id
        request = self._prepare_request()
        response = session.delete(request.url,
                                  json=body)
        try:
            self._translate_response(response, has_body=True)
        except exceptions.ResourceNotFound:
            if ignore_missing:
                return None
            raise
        return self

    def expand_replication(self, session,
                           replication, new_size):
        """Method to expand replication pair

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str replication: ID of replication pair
            which will be expanded
        :param int new_size: Replication pair new size
        """
        url = utils.urljoin(self.base_path,
                            replication,
                            'action')
        body = {
            'extend-replication': {
                'new_size': new_size
            }
        }

        return session.post(url, json=body)
