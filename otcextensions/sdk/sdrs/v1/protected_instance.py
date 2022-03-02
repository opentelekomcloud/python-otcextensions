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


class Attachment(resource.Resource):
    #: Properties
    #: Replication pair ID
    replication = resource.Body('replication')
    #: Protected instance attached disk name
    device = resource.Body('device')


class Metadata(resource.Resource):
    #: Properties
    #: Resource status (frozen or not)
    system_frozen = resource.Body('__system__frozen',
                                  type=bool)


class TagSpec(resource.Resource):
    #: Properties
    #: Tag key
    key = resource.Body('key')
    #: Tag value
    value = resource.Body('value')


class ProtectedInstance(resource.Resource):
    """SDRS Protected Instance Resource"""
    resource_key = 'protected_instance'
    resources_key = 'protected_instances'
    base_path = '/protected-instances'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'availability_zone', 'limit', 'marker', 'name', 'offset',
        'protected_instance_ids', 'query_type', 'server_group_id',
        'server_group_ids', 'status')

    #: Properties
    #: Attached replication pair info
    attachment = resource.Body('attachment', type=list, list_type=Attachment)
    #: Creation time
    created_at = resource.Body('created_at')
    #: Protected instance description
    description = resource.Body('description')
    #: Specifies whether to delete EIP on DR site server
    #: Default: False
    delete_target_eip = resource.Body('delete_target_eip', type=bool)
    #: Specifies whether to delete server on DR site server
    #: Default: False
    delete_target_server = resource.Body('delete_target_server', type=bool)
    #: DR site server flavor ID
    flavorRef = resource.Body('flavorRef')
    #: Protected instance ID
    id = resource.Body('id')
    #: Created task job ID
    job_id = resource.Body('job_id')
    #: Protected instance metadata
    metadata = resource.Body('metadata', type=Metadata)
    #: Protected instance name
    name = resource.Body('name')
    #: Network ID of the subnet for primary NIC on
    #: DR site server
    primary_subnet_id = resource.Body('primary_subnet_id')
    #: IP address of the primary NIC on DR site server
    primary_ip_address = resource.Body('primary_ip_address')
    #: Production site of protection group
    priority_station = resource.Body('priority_station')
    #: Protected instance synch progress
    progress = resource.Body('progress', type=int)
    #: Protection group ID
    server_group_id = resource.Body('server_group_id')
    #: Production site ECS ID
    server_id = resource.Body('server_id')
    #: Production site server ID
    source_server = resource.Body('source_server')
    #: Protected instance status
    status = resource.Body('status')
    #: Instance tag list
    tags = resource.Body('tags', type=list, list_type=TagSpec)
    #: DR site server ID
    target_server = resource.Body('target_server')
    #: Update time
    updated_at = resource.Body('updated_at')

    def delete(self, session, error_message=None,
               delete_target_server=False, delete_target_eip=False):
        """Delete the remote resource based on this instance.

        This function overrides default Resource.delete to enable params

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param bool delete_target_server: Specifies whether target
            ECS should be deleted after protection group deletion
        :param bool delete_target_eip: Specifies whether target
            ECS should be deleted after protection group deletion

        :return: This :class:`Group` instance.
        """
        body = {
            'delete_target_server': delete_target_server,
            'delete_target_eip': delete_target_eip
        }
        request = self._prepare_request()
        response = session.delete(request.url,
                                  json=body)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message
        self._translate_response(response, has_body=True, **kwargs)
        return self

    def attach_pair(self, session, protected_instance,
                    replication_id, device='/dev/vdb'):
        """Method to attach replication pair to the specified
            protected instance

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protected_instance: ID of protected instance
            on which replication pair will be attached
        :param str replication_id: ID of replication pair to be
            attached
        :param str device: disk device name of a replication pair
        """
        url = utils.urljoin(self.base_path,
                            protected_instance,
                            'attachreplication')
        body = {
            "replicationAttachment": {
                "replication_id": replication_id,
                "device": device
            }
        }

        return session.post(url, json=body)

    def detach_pair(self, session, protected_instance,
                    replication_id):
        """Method to detach replication pair from the specified
            protected instance

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protected_instance: ID of protected instance
            from which replication pair will be detached
        :param str replication_id: ID of replication pair to be
            detached
        """
        url = utils.urljoin(self.base_path,
                            protected_instance,
                            'detachreplication',
                            replication_id)

        return session.delete(url)

    def add_nic(self, session, protected_instance, subnet_id,
                security_groups=None, ip_address=None):
        """Method to add NIC to protected instance

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protected_instance: ID of protected instance
            for which NIC will be added
        :param str subnet_id: Subnet ID of the NIC to be added
        :param list security_groups: list of security groups
            to be added for NIC in format 'id': 'value'
        :param str ip_address: IP address of NIC
        """
        body = {
            'subnet_id': subnet_id
        }
        if security_groups:
            body['security_groups'] = security_groups
        if ip_address:
            body['ip_address'] = ip_address

        url = utils.urljoin(self.base_path,
                            protected_instance,
                            'nic')
        return session.post(url, json=body)

    def delete_nic(self, session, protected_instance,
                   nic_id):
        """Method to remove NIC to protected instance

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protected_instance: ID of protected instance
            for which NIC will be added
        :param str nic_id: ID of Network interface card
        """
        body = {
            'nic_id': nic_id
        }
        url = utils.urljoin(self.base_path,
                            protected_instance,
                            'nic/delete')
        return session.post(url, json=body)

    def modify_instance(self, session,
                        protected_instance, flavor=None,
                        production_flavor=None, dr_flavor=None):
        """Method to modify server specifications

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protected_instance: ID of protected instance
        :param str flavor: flavor ID for both production and DR sites
        :param str production_flavor: flavor ID for production site
            If 'flavor' is specified this parameter doesn't take effect
        :param str dr_flavor: flavor ID for DR site
            If 'flavor' is specified this parameter doesn't take effect
        """
        body = {
            'resize': {}
        }
        if flavor:
            body['resize']['flavorRef'] = flavor
        if production_flavor:
            body['resize']['production_flavorRef'] = production_flavor
        if dr_flavor:
            body['resize']['dr_flavorRef'] = dr_flavor

        url = utils.urljoin(self.base_path,
                            protected_instance,
                            'resize')
        return session.post(url, json=body)
