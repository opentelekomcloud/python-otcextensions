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


class Route(resource.Resource):
    resources_key = 'routes'
    resource_key = 'route'
    base_path = '/vpc/routes'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'marker', 'limit', 'type', 'router_id',
        'destination', 'project_id', project_id='tenant_id',
        router_id='vpc_id'
    )

    #: Specifies the VPC peering connection ID.
    #: *Type: uuid*
    id = resource.Body('id')
    #: Specifies the next hop.
    #:  If the route type is peering, enter the VPC peering connection ID.
    nexthop = resource.Body('nexthop')
    #: Specifies the destination address in the CIDR notation format,
    #:  for example, 192.168.200.0/24.
    destination = resource.Body('destination')
    #: Specifies the route type. Currently, the value can only be peering.
    type = resource.Body('type')
    #: Specifies the Router of the route.
    #:  Set this parameter to the existing Router ID.
    router_id = resource.Body('vpc_id')
    #: Specifies the project ID.
    project_id = resource.Body('tenant_id')
