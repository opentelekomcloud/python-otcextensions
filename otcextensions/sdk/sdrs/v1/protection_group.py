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


class ProtectionGroup(resource.Resource):
    """SDRS Protection Group Resource"""
    resource_key = 'server_group'
    resources_key = 'server_groups'
    base_path = '/server-groups'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'availability_zone', 'limit', 'name', 'offset',
        'query_type', 'status')

    #: Properties
    #: Creation time
    created_at = resource.Body('created_at')
    #: Protection group description
    description = resource.Body('description')
    #: Number of DR drills in a protection group.
    disaster_recovery_drill_num = resource.Body('disaster_recovery_drill_num',
                                                type=int)
    #: Active-active domain ID
    domain_id = resource.Body('domain_id')
    #: Active-active domain name
    domain_name = resource.Body('domain_name')
    #: Disaster recovery type
    #: Default: migration
    dr_type = resource.Body('dr_type')
    #: Protection group health status
    health_status = resource.Body('health_status')
    #: Protection group ID
    id = resource.Body('id')
    #: Executed task job ID
    job_id = resource.Body('job_id')
    #: Protection group name
    name = resource.Body('name')
    #: Production site of protection group
    priority_station = resource.Body('priority_station')
    #: Protection group synchronization progress
    progress = resource.Body('progress', type=int)
    #: Number of protected instances in protection group
    protected_instance_num = resource.Body('protected_instance_num', type=int)
    # Specifies whether protection group is enabled
    protected_status = resource.Body('protected_status')
    #: Protection mode
    protection_type = resource.Body('protection_type')
    #: Reserved protection parameter
    replication_model = resource.Body('replication_model')
    #: Number of replication pairs in protection group
    replication_num = resource.Body('replication_num', type=int)
    #: Replication group data synchronization status
    replication_status = resource.Body('replication_status')
    #: Type of managed servers
    server_type = resource.Body('server_type')
    #: Production site AZ
    source_availability_zone = resource.Body('source_availability_zone')
    #: Production site VPC ID
    source_vpc_id = resource.Body('source_vpc_id')
    #: Protection group status
    status = resource.Body('status')
    #: Disaster recovery site AZ
    target_availability_zone = resource.Body('target_availability_zone')
    #: Disaster recovery site VPC ID
    target_vpc_id = resource.Body('target_vpc_id')
    #: DR drill VPC ID
    test_vpc_id = resource.Body('test_vpc_id')
    #: Update time
    updated_at = resource.Body('updated_at')

    def enable_protection_group(self, session, protection_group):
        """Method to enable protection for protection group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protection_group: ID of protection group to
        be enabled
        """
        url = utils.urljoin(self.base_path, protection_group, '/action')
        body = {
            'start-server-group': {}
        }
        return session.post(url, json=body)

    def disable_protection_group(self, session, protection_group):
        """Method to disable protection for protection group

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protection_group: ID of protection group to
        be disabled
        """
        url = utils.urljoin(self.base_path, protection_group, '/action')
        body = {
            'stop-server-group': {}
        }
        return session.post(url, json=body)

    def perform_failover(self, session, protection_group):
        """Method to perform failover from production site to
        DR site

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protection_group: ID of protection group to
        perform failover
        """
        url = utils.urljoin(self.base_path, protection_group, '/action')
        body = {
            'failover-server-group': {}
        }
        return session.post(url, json=body)

    def perform_planned_failover(self, session, protection_group,
                                 priority_station):
        """Method to perform planned failover from production site
        to DR site

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str protection_group: ID of protection group to
        perform planned failover
        :param str priority_station: direction of planned failover
        Values: source of target
        """
        url = utils.urljoin(self.base_path, protection_group, '/action')
        body = {
            "reverse-server-group": {
                "priority_station": priority_station
            }
        }

        return session.post(url, json=body)
