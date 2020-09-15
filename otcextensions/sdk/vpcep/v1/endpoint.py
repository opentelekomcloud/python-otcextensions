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


class Endpoint(resource.Resource):
    resources_key = 'endpoints'
    base_path = '/vpc-endpoints'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'endpoint_service_name', 'vpc_id', 'id',
        'limit', 'offset', 'sort_key', 'sort_dir'
    )

    # Properties
    #: Specifies the name of the VPC endpoint service.
    endpoint_service_name = resource.Body('endpoint_service_name')
    #: Specifies the ID of the VPC endpoint service.
    endpoint_service_id = resource.Body('endpoint_service_id')
    #: Specifies the unique ID of the VPC endpoint.
    id = resource.Body('id')
    #: Specifies the ID of the VPC where the VPC endpoint is to be created.
    vpc_id = resource.Body('vpc_id')
    #: Specifies the ID of the subnet created in the VPC specified
    #:  by vpc_id. The value is in the UUID format.
    subnet_id = resource.Body('subnet_id')
    #: Specifies the status of the VPC endpoint service.
    status = resource.Body('status')
    #: Specifies the sorting field of the VPC endpoint list.
    sort_key = resource.Body('sort_key')
    #: Specifies the sorting method of the VPC endpoint list.
    sort_dir = resource.Body('sort_dir')
    #: Specifies the maximum number of VPC endpoints displayed on each page.
    limit = resource.Body('limit', type=int)
    #: Specifies the offset.
    offset = resource.Body('offset', type=int)

    #: Specifies the type of the VPC endpoint service that is
    #:  associated with the VPC endpoint.
    service_type = resource.Body('service_type')
    #: Specifies the connection status of the VPC endpoint.
    status = resource.Body('status')
    #: Specifies the domain status.
    active_status = resource.Body('active_status')
    #: Specifies the packet ID of the VPC endpoint.
    marker_id = resource.Body('marker_id', type=int)
    #: Specifies whether to create a private domain name.
    enable_dns = resource.Body('enable_dns', type=bool)
    #: Specifies the domain name for accessing the associated
    #:  VPC endpoint service.
    dns_names = resource.Body('dns_names', type=list)
    #: Specifies the IP address for accessing the associated
    #:  VPC endpoint service.
    ip = resource.Body('ip')
    #: Specifies the creation time of the VPC endpoint.
    created_at = resource.Body('created_at')
    #: Specifies the update time of the VPC endpoint.
    updated_at = resource.Body('updated_at')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Lists the resource tags.
    tags = resource.Body('tags', type=list, list_type=Tag)
    #: Specifies the error message.
    error = resource.Body('error', type=list, list_type=Error)
    #: Specifies the whitelist for controlling access to the VPC endpoint.
    whitelist = resource.Body('whitelist', type=list)
    #: Specifies whether to enable access control.
    enable_whitelist = resource.Body('enable_whitelist', type=bool)
    #: Lists the IDs of route tables.
    routetables = resource.Body('routetables', type=list)
