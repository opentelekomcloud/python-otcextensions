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


class DRDrill(resource.Resource):
    """SDRS Disaster recovery Drill Resource"""
    resource_key = 'disaster_recovery_drill'
    resources_key = ''
    base_path = '/disaster-recovery-drills'

    # capabilities
    #allow_create = True
    #allow_list = True
    #allow_fetch = True
    #allow_delete = True
    #allow_commit = True

    # _query_mapping = resource.QueryParameters(
    #     'availability_zone', 'limit', 'marker', 'name', 'offset',
    #     'protected_instance_id', 'protected_instance_ids', 'query_type',
    #     'server_group_id', 'server_group_ids', 'status')

    #: Properties
    #: DR drill VPC ID
    drill_vpc_id = resource.Body('drill_vpc_id')
    #: Job ID
    job_id = resource.Body('job_id')
    #: DR drill name
    name = resource.Body('name')
    #: Protection group ID
    server_group_id = resource.Body('server_group_id')
