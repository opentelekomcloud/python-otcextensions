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


class DirectConnectEndpointGroup(resource.Resource):

    base_path = '/dcaas/dc-endpoint-groups'
    resource_key = 'dc_endpoint_group'
    resources_key = 'dc_endpoint_groups'

    # capabilities
    allow_list = True
    allow_fetch = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'id', 'project_id', 'name', 'description', 'endpoints', 'type',
        projrct_id='tenant_id'
    )

    # Properties
    #: The ID of the Direct Connect Endpoint Group.
    id = resource.Body('id')
    #: The name of the Direct Connect Endpoint Group.
    name = resource.Body('name')
    #: Provides supplementary information about the Direct Connect Endpoint
    # Group.
    description = resource.Body('description')
    #: The list of the endpoints in a Direct Connect Endpoint Group
    endpoints = resource.Body('endpoints', type=list)
    #: The type of the Direct Connect Endpoints. The value can only be cidr.
    type = resource.Body('type')
    #: The project ID.
    project_id = resource.Body('tenant_id')
