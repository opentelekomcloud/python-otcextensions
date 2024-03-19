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


class VpcEndpoint(resource.Resource):
    resources_key = 'endpoints'
    resource_key = None
    base_path = '/v1/%(project_id)s/vpc-endpoints'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'offset', 'limit', 'router_id',
        'endpoint_service_name', router_id='vpc_id'
    )

    # Properties
    #: Specifies information about the service type.
    service_type = resource.Body('service_type')
    #: Specifies the status.
    status = resource.Body('status')
    #: Specifies the domain status.
    active_status = resource.Body('active_status')
    #: Specifies the endpoint service name.
    endpoint_service_name = resource.Body('endpoint_service_name')
    #: Specifies the endpoint service id.
    endpoint_service_id = resource.Body('endpoint_service_id')
    #: Specifies the marker id.
    marker_id = resource.Body('marker_id', type=int)
    #: Specifies the endpoint ip address.
    ip = resource.Body('ip')
    #: Specifies the router id.
    vpc_id = resource.Body('vpc_id')
    #: Specifies the subnet id.
    subnet_id = resource.Body('subnet_id')
    #: Specifies the project id.
    project_id = resource.URI('project_id')
    #: Specifies if whitelist is enabled.
    enable_whitelist = resource.Body('enable_whitelist',
                                     type=bool,
                                     default=False)
    #: Specifies the whitelist.
    whitelist = resource.Body('whitelist', type=list)
    #: Specifies if dns is enabled.
    enable_dns = resource.Body('enable_dns', type=bool, default=False)
    #: Specifies the dns names.
    dns_names = resource.Body('dns_names', type=list)
    #: Specifies the route tables.
    routetables = resource.Body('routetables', type=list)
    #: Provides supplementary information about the VPC peering connection.
    description = resource.Body('description')
    #: Specifies the time (UTC) when the VPC peering connection is created.
    #:  Format is *yyyy-mm-dd hh:mm:ss*.
    created_at = resource.Body('created_at')
    #: Specifies the time (UTC) when the VPC peering connection is updated.
    #:  Format is *yyyy-mm-dd hh:mm:ss*.
    updated_at = resource.Body('updated_at')
