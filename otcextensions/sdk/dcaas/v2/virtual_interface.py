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


class VirtualInterface(resource.Resource):

    resource_key = 'virtual_interface'
    resources_key = 'virtual_interfaces'
    base_path = '/dcaas/virtual-interfaces'

    # capabilities
    allow_list = True
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'id', 'project_id', 'name', 'description', 'direct_conect_id', 'vgw_id',
        'type', 'service_type', 'vlan', 'bandwidth', 'local_gateway_v4_ip',
        'remote_gateway_v4_ip', 'route_mode', 'bgp_asn', 'bgp_md5',
        'remote_ep_group_id', 'service_ep_group_id', 'admin_state_up',
        'create_time', 'delete_time', 'status', 'rate_limit',
        project_id='tenant_id')

    # Properties
    #: ID of the direct connection.
    id = resource.Body('id')
    #: Indicates the virtual interface name.
    name = resource.Body('name')
    #: Project id.
    project_id = resource.Body('tenant_id')
    #: Indicates the description of the virtual interface.
    description = resource.Body('description')
    #: Specifies the connection ID.
    direct_connect_id = resource.Body('direct_connect_id')
    #: Specifies the virtual gateway ID.
    vgw_id = resource.Body('vgw_id')
    #: Specifies the virtual interface type. The value can be public or private.
    type = resource.Body('type')
    #: Specifies the access service type. The value can be vpc, public service, or vpc and public service.
    service_type = resource.Body('service_type')
    #: Specifies the VLAN used by the local gateway to communicate with the remote gateway.
    vlan = resource.Body('vlan', type=int)
    #: Specifies the virtual interface bandwidth.
    bandwidth = resource.Body('bandwidth', type=int)
    #: Specifies the IPv4 address of the local gateway.
    local_gateway_v4_ip = resource.Body('local_gateway_v4_ip')
    #: Specifies the IPv4 address of the remote gateway.
    remote_gateway_v4_ip = resource.Body('remote_gateway_v4_ip')
    #: Specifies the routing mode. The value can be static or bgp.
    route_mode = resource.Body('route_mode')
    #: Specifies the AS number of the BGP peer.
    bgp_asn = resource.Body('bgp_asn', type=int)
    #: Specifies the MD5 password of the BGP peer.
    bgp_md5 = resource.Body('bgp_md5')
    #: Specifies the ID of the remote endpoint group that records the tenant CIDR blocks.
    remote_ep_group_id = resource.Body('remote_ep_group_id')
    #: Specifies the ID of the service endpoint group that records the public service CIDR blocks.
    service_ep_group_id = resource.Body('service_ep_group_id')
    #: Specifies the time when the virtual interface is created.
    create_time = resource.Body('create_time')
    #: Specifies the time when the virtual interface is deleted.
    delete_time = resource.Body('delete_time')
    #: Specifies the administrative status of the virtual interface.\
    # The value can be true or false.
    admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies whether to limit the traffic rate. The value can be true or false.
    rate_limit = resource.Body('rate_limit', type=bool)
    #: Specifies the virtual interface status. The value can be ACTIVE, DOWN, BUILD, ERROR, PENDING_CREATE,
    #PENDING_UPDATE, or PENDING_DELETE.
    status = resource.Body('status')
