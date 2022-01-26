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


class VirtualGateway(resource.Resource):

    resource_key = 'virtual_gateway'
    resources_key = 'virtual_gateways'
    base_path = '/dcaas/virtual-gateways'

    # capabilities
    allow_list = True
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'project_id', 'name', 'vpc_id', 'local_ep_group_id', 'device_id',
        'redundant_device_id', 'type', 'ipsec_bandwidth', 'bgp_asn',
        'admin_state_up', project_id='tenant_id')

    # Properties
    #: ID of the direct connection.
    id = resource.Body('id')
    #: Indicates the virtual gateway name.
    name = resource.Body('name')
    #: Indicates the description of the virtual gateway.
    description = resource.Body('description')
    #: Specifies the ID of the VPC to be accessed.
    vpc_id = resource.Body('vpc_id')
    #: Specifies the ID of the local endpoint group that records CIDR blocks
    # of the VPC subnets.
    local_ep_group_id = resource.Body('local_ep_group_id')
    #: Specifies the ID of the physical device used by the virtual gateway.
    device_id = resource.Body('device_id')
    #: Specifies the ID of the redundant physical device used by
    # the virtual gateway.
    redundant_device_id = resource.Body('redundant_device_id')
    #: Specifies the virtual gateway type. The value can be default
    # or double ipsec.
    type = resource.Body('type')
    #: Specifies the bandwidth provided for IPsec VPN in Mbit/s.
    ipsec_bandwidth = resource.Body('ipsec_bandwidth')
    #: Specifies the BGP ASN of the virtual gateway.
    bgp_asn = resource.Body('bgp_asn', type=int)
    #: Specifies the administrative status of the virtual gateway.\
    # The value can be true or false.
    admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the virtual gateway status. The value can be ACTIVE, DOWN,
    # BUILD, ERROR, PENDING_CREATE, PENDING_UPDATE, or PENDING_DELETE.
    status = resource.Body('status')
