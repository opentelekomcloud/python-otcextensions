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


class DrillServers(resource.Resource):
    #: Properties
    #: Protected instance ID of drill server
    protected_instance = resource.Body('protected_instance')
    #: Drill server ID
    drill_server_id = resource.Body('drill_server_id')


class DRDrill(resource.Resource):
    """SDRS Disaster recovery Drill Resource"""
    resource_key = 'disaster_recovery_drill'
    resources_key = 'disaster_recovery_drills'
    base_path = '/disaster-recovery-drills'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'drill_vpc_id', 'limit', 'marker', 'name',
        'offset', 'server_group_id', 'status')

    #: Properties
    #: Creation time
    created_at = resource.Body('created_at')
    #: Drill servers information
    drill_servers = resource.Body('drill_servers', type=list, list_type=DrillServers)
    #: DR drill VPC ID
    drill_vpc_id = resource.Body('drill_vpc_id')
    #: Job ID
    job_id = resource.Body('job_id')
    #: DR drill ID
    id = resource.Body('id')
    #: DR drill name
    name = resource.Body('name')
    #: Protection group ID
    server_group_id = resource.Body('server_group_id')
    #: DR drill status
    status = resource.Body('status')
    #: Update time
    updated_at = resource.Body('updated_at')
