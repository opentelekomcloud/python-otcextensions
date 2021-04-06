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


class Port(resource.Resource):
    #: Specifies the port for accessing the VPC endpoint.
    client_port = resource.Body('client_port', type=int)
    #: Specifies the port for accessing the VPC endpoint service.
    server_port = resource.Body('server_port', type=int)
    #: Specifies the protocol used in port mappings.
    #:  The value can be TCP or UDP.
    protocol = resource.Body('protocol')


class Tag(resource.Resource):
    #: Specifies the tag key. A tag key contains a maximum of 36
    #:  Unicode characters.
    key = resource.Body('key')
    #: Specifies the tag value. A tag value contains a maximum of 43 Unicode
    value = resource.Body('value')


class Error(resource.Resource):
    #: Specifies the error code.
    error_code = resource.Body('error_code')
    #: Specifies the error message.
    error_message = resource.Body('error_message')


class EndpointService(resource.Resource):
    resources_key = 'endpoint_services'
    base_path = '/vpc-endpoint-services'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'sort_key', 'sort_dir', 'limit',
        'offset', 'status', name='endpoint_service_name'
    )

    # Properties
    #: Specifies the name of the VPC endpoint service.
    #:  The value is not case-sensitive and supports fuzzy match.
    endpoint_service_name = resource.Body('endpoint_service_name')
    #: Specifies the unique ID of the VPC endpoint service.
    id = resource.Body('id')
    #: Specifies the status of the VPC endpoint service.
    status = resource.Body('status')
    #: Specifies the sorting field of the VPC endpoint service list.
    sort_key = resource.Body('sort_key')
    #: Specifies the sorting method of the VPC endpoint service list.
    sort_dir = resource.Body('sort_dir')
    #: Specifies the maximum number of VPC endpoint services
    #:  displayed on each page.
    limit = resource.Body('limit', type=int)
    #: Specifies the offset.
    offset = resource.Body('offset', type=int)

    #: Specifies the ID for identifying the backend resource of the
    #:  VPC endpoint service. The ID is in the form of the UUID.
    port_id = resource.Body('port_id')
    #: Specifies the ID of the virtual NIC to which the virtual IP
    #:  address is bound. This parameter is returned only when
    #:  port_id is set to VIP.
    vip_port_id = resource.Body('vip_port_id')
    #: Specifies the ID of the cluster associated with the
    #:  target VPCEP resource.
    pool_id = resource.Body('pool_id')
    #: Specifies the name of the VPC endpoint service.
    service_name = resource.Body('service_name')
    #: Specifies the resource type.
    server_type = resource.Body('server_type')
    #: Specifies the ID of the VPC to which the backend resource of
    #:  the VPC endpoint service belongs.
    router_id = resource.Body('vpc_id')
    #: Specifies whether connection approval is required.
    approval_enabled = resource.Body('approval_enabled', type=bool)
    #: Specifies the type of the VPC endpoint service.
    service_type = resource.Body('service_type')
    #: Specifies the creation time of the VPC endpoint service.
    created_at = resource.Body('created_at')
    #: Specifies the update time of the VPC endpoint service.
    updated_at = resource.Body('updated_at')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the network segment type.
    cidr_type = resource.Body('cidr_type')
    #: Lists the port mappings opened to the VPC endpoint service.
    ports = resource.Body('ports', type=list, list_type=Port)
    #: Lists the resource tags.
    tags = resource.Body('tags', type=list, list_type=Tag)
    #: Specifies the number of Creating or Accepted VPC endpoints
    #:  under the VPC endpoint service.
    connection_count = resource.Body('connection_count', type=int)
    #: This parameter is available only when the server can parse
    #:  fields tcp option and tcp payload.
    tcp_proxy = resource.Body('tcp_proxy')
    #: Specifies the error message.
    #:  This field is returned when the status of the VPC endpoint
    #:  service changes to failed.
    error = resource.Body('error', type=list, list_type=Error)


class Connection(resource.Resource):
    resources_key = 'connections'
    base_path = '/vpc-endpoint-services/%(endpoint_service_id)s/connections'

    # capabilities
    allow_list = True

    endpoint_service_id = resource.URI('endpoint_service_id')

    _query_mapping = resource.QueryParameters(
        'id', 'marker_id', 'sort_key', 'sort_dir', 'limit', 'offset'
    )

    # Properties
    #: Specifies the unique ID of the VPC endpoint.
    id = resource.Body('id')
    #: Specifies the packet ID of the VPC endpoint.
    marker_id = resource.Body('marker_id')
    #: Specifies the creation time of the VPC endpoint.
    created_at = resource.Body('created_at')
    #: Specifies the update time of the VPC endpoint.
    updated_at = resource.Body('updated_at')
    #: Specifies the user's domain ID.
    domain_id = resource.Body('domain_id')
    #: Specifies the connection status of the VPC endpoint.
    status = resource.Body('status')


class ManageConnection(resource.Resource):
    base_path = ('/vpc-endpoint-services/%(endpoint_service_id)s'
                 '/connections/action')

    # capabilities
    allow_create = True

    endpoint_service_id = resource.URI('endpoint_service_id')

    #: Lists the VPC endpoints.
    endpoints = resource.Body('endpoints', type=list)
    #: List the connections.
    connections = resource.Body('connections', type=list, list_type=Connection)
    #: Specifies the operation to be performed.
    action = resource.Body('action')


class Whitelist(resource.Resource):
    resources_key = 'permissions'
    base_path = '/vpc-endpoint-services/%(endpoint_service_id)s/permissions'

    endpoint_service_id = resource.URI('endpoint_service_id')

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'sort_key', 'sort_dir', 'limit', 'offset'
    )

    # Properties
    #: Specifies the unique ID of the permission.
    id = resource.Body('id')
    #: whitelist record.
    permission = resource.Body('permission')
    #: Indicates the time of adding the whitelist record.
    created_at = resource.Body('created_at')


class ManageWhitelist(resource.Resource):
    base_path = ('/vpc-endpoint-services/%(endpoint_service_id)s'
                 '/permissions/action')

    # capabilities
    allow_create = True

    endpoint_service_id = resource.URI('endpoint_service_id')

    # Properties
    #: Lists the whitelist records.
    permissions = resource.Body('permissions', type=list)
    #: Specifies the operation to be performed.
    action = resource.Body('action')
