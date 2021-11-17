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


class VPC(resource.Resource):
    resource_key = 'vpc'
    resources_key = 'vpcs'
    base_path = '/vpcs'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'name', 'description', 'cidr', 'vpc_id',
        'project_id', project_id='tenant_id'
    )

    # Properties
    # Specifies the VPC name.
    name = resource.Body('name')
    # Provides supplementary information about the VPC.
    description = resource.Body('description')
    # Specifies the available IP address ranges for subnets in the VPC.
    cidr = resource.Body('cidr')
    # Specifies the route list.
    routes = resource.Body('routes')
    # Specifies whether the shared SNAT function is enabled.
    enable_shared_snat = resource.Body('enable_shared_snat')
