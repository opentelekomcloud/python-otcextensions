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
from openstack import resource


class TagsSpec(resource.Resource):
    #: Specifies the tag key.
    key = resource.Body('key')
    #: Specifies the tag value.
    value = resource.Body('value')


class Endpoint(resource.Resource):
    base_path = '/vpc-endpoints'
    resources_key = 'endpoints'
    resource_key = None

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id',
        'offset',
        'limit',
        'router_id',
        'endpoint_service_name',
        'sort_dir',
        'sort_key',
        router_id='vpc_id',
    )

    # Properties
    #: Domain status.
    active_status = resource.Body('active_status', type=list)
    #: Creation time of the VPC endpoint.
    created_at = resource.Body('created_at')
    #: Description of the VPC endpoint.
    description = resource.Body('description')
    #: Domain name for accessing the associated VPC endpoint service.
    dns_names = resource.Body('dns_names', type=list)
    #: Whether the VPC endpoint is enabled.
    enable_status = resource.Body('enable_status')
    #: ID of the cluster associated with the VPC endpoint.
    endpoint_pool_id = resource.Body('endpoint_pool_id')
    #: ID of the VPC endpoint service.
    endpoint_service_id = resource.Body('endpoint_service_id')
    #: Name of the VPC endpoint service.
    endpoint_service_name = resource.Body('endpoint_service_name')
    #: VPC endpoint ID.
    id = resource.Body('id')
    #: IP address for accessing the associated VPC endpoint service.
    ip = resource.Body('ip')
    #: Whether to create a private domain name.
    is_dns_enabled = resource.Body('enable_dns', type=bool)
    #: Whether access control is enabled.
    is_whitelist_enabled = resource.Body('enable_whitelist', type=bool)
    #: Packet ID of the VPC endpoint.
    marker_id = resource.Body('marker_id', type=int)
    #: Specifies the ID of the network in the VPC/Router.
    network_id = resource.Body('subnet_id')
    #: Project ID.
    project_id = resource.Body('project_id')
    #: IDs of route tables.
    route_tables = resource.Body('routetables', type=list)
    #: ID of the VPC/Router where the VPC endpoint is to be created.
    router_id = resource.Body('vpc_id')
    #: Type of the VPC endpoint service that is associated with the
    #:  VPC endpoint.
    service_type = resource.Body('service_type')
    #: Specifies the name of the VPC endpoint specifications.
    specification_name = resource.Body('specification_name')
    #: Specifies the connection status of the VPC endpoint.
    status = resource.Body('status')
    #: Lists the resource tags.
    tags = resource.Body('tags', type=list, list_type=TagsSpec)
    #: Update time of the VPC endpoint.
    updated_at = resource.Body('updated_at')
    #: Whitelist for controlling access to the VPC endpoint.
    whitelist = resource.Body('whitelist', type=list)
