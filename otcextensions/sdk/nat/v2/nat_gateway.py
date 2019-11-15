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

class NatGateway(resource.Resource):
    resources_key = 'nat_gateways'
    resource_key = 'nat_gateway'
    base_path = '/nat_gateways'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True
    
    # Properties
    #: Specifies the ID of the NAT gateway.
    id = resource.Body('id')
    #: Specifies the project ID
    tenant_id = resource.Body('tenant_id')
    #: Specifies the name of the NAT gateway.
    #: Contains only digits, letters, underscores and hyphens
    name = resource.Body('name')
    #: Provides description of NAT Gateway
    description = resource.Body('description')
    #: Specifies the type of the NAT gateway.
    #: *1:* small type, supports up to 10,000 SNAT connections
    #: *2:* medium type, supports up to 50,000 SNAT connections
    #: *3:* large type, supports up to 200,000 SNAT connections
    #: *4:* extra-large type, supports up to 1,000,000 SNAT connections
    spec = resource.Body('spec')
    #: Specifies the router ID
    router_id = resource.Body('router_id')
    #: Specifies the network ID of the downstream interface
    internal_network_id = resource.Body('internal_network_id')
    #: Specifies the status
    status = resource.Body('status')
    #: Specifies whether GW is up or down
    #: *true:* Gw is up
    #: *false:* GW is down
    admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies when GW was is created
    #: format is *yyyy-mm-dd hh:mm:ss*
    created_at = resource.Body('created_at')

    
