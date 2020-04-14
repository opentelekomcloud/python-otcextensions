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

class Snat(resource.Resource):
    resources_key = 'snat_rules'
    base_path = '/snat_rules'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True
    
    # Properties
    id = resource.Body('id')
    #: Specifies the ID of the SNAT rule.
    tenant_id = resource.Body('tenant_id')
    #: Specifies the project ID.
    nat_gateway_id = resource.Body('nat_gateway_id')
    #: Specifies the NAT Gateway ID.
    network_id = resource.Body('network_id')
    #: Specifies the network ID
    cidr = resource.Body('cidr')
    #: Specifies a subset of the VPC subnet CIDR block or a 
    #: CIDR block of Direct Connect connection.
    source_type = resource.Body('source_type', type=int)
    #: *0:* Either network_id or cidr can be specified in VPC
    #: *1:* only cidr can be specified over a Direct Connect connection
    #: Default: 0
    floating_ip_id = resource.Body('floating_ip_id')
    #: Specifies the EIP ID
    #: Multiple EIPs are separated using commas
    floating_ip_address = resource.Body('floating_ip_address')
    #: Specifies the EIP
    #: Multiple EIPs are separated using commas
    status = resource.Body('status')
    #: Specifies the status of the SNAT rule
    admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies whether SNAT rule is enabled / disabled
    #: *true:* SNAT rule is enabled
    #: *false:* SNAT rule is disabled
    created_at = resource.Body('created_at')
    #: Specifies when the rule is created.
    #: The format is yyyy-mm-dd hh:mm:ss.