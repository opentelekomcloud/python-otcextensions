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


class LoadBalancer(resource.Resource):
    resource_key = 'loadbalancer'
    resources_key = 'loadbalancers'
    base_path = '/elb/loadbalancers'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'availability_zone_list', 'description',
        'flavor_id', 'name', 'project_id', 'provider',
        'provisioning_status', 'operating_status',
        'vip_address', 'vip_network_id',
        'vip_port_id', 'vip_subnet_id',
        'vip_qos_policy_id',
        is_admin_state_up='admin_state_up',
        availability_zones='availability_zone_list',
    )

    # Properties
    #: Name of the target Octavia availability zone
    availability_zones = resource.Body('availability_zone_list', type=list)
    #: Billing information about the load balancer.
    billing_info = resource.Body('billing_info')
    #: Timestamp when the load balancer was created
    created_at = resource.Body('created_at')
    #: The load balancer description
    description = resource.Body('description')
    #: EIP bound to the load balancer.
    eips = resource.Body('eips', type=list, list_type=dict)
    #: The load balancer flavor ID
    flavor_id = resource.Body('flavor_id')
    #: Specifies whether the load balancer is a dedicated load balancer.
    guaranteed = resource.Body('guaranteed')
    #: The administrative state of the load balancer *Type: bool*
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: The Layer-4 flavor.
    l4_flavor_id = resource.Body('l4_flavor_id')
    #: Reserved Layer 4 flavor.
    l4_scale_flavor_id = resource.Body('l4_scale_flavor_id')
    #: Specifies the Layer-7 flavor.
    l7_flavor_id = resource.Body('l7_flavor_id')
    #: Reserved Layer 7 flavor.
    l7_scale_flavor_id = resource.Body('l7_scale_flavor_id')
    #: List of listeners associated with this load balancer
    listeners = resource.Body('listeners', type=list, list_type=dict)
    #: Operating status of the load balancer
    operating_status = resource.Body('operating_status')
    #: List of pools associated with this load balancer
    pools = resource.Body('pools', type=list, list_type=dict)
    #: The ID of the project this load balancer is associated with.
    project_id = resource.Body('project_id')
    #: Provider name for the load balancer.
    provider = resource.Body('provider')
    #: The provisioning status of this load balancer
    provisioning_status = resource.Body('provisioning_status')
    #: Timestamp when the load balancer was last updated
    updated_at = resource.Body('updated_at')
    #: VIP address of load balancer
    vip_address = resource.Body('vip_address')
    #: VIP netowrk ID
    vip_network_id = resource.Body('vip_network_id')
    #: VIP port ID
    vip_port_id = resource.Body('vip_port_id')
    #: VIP subnet ID
    vip_subnet_id = resource.Body('vip_subnet_cidr_id')
    # VIP qos policy id
    vip_qos_policy_id = resource.Body('vip_qos_policy_id')
    #: Tags added to the load balancer
    tags = resource.Body('tags', type=list)

    #: Network id
    network_ids = resource.Body('elb_virsubnet_ids', type=list)
    #: FIP
    floating_ip = resource.Body('publicip', type=list, list_type=dict)
    #: Assigned FIPs
    floating_ips = resource.Body('publicips', type=list, list_type=dict)
    #: Router id
    vpc_id = resource.Body('vpc_id')
    #: Specifies whether to enable cross-VPC backend.
    ip_target_enable = resource.Body('ip_target_enable')
    #: IPv6 vip address
    ipv6_vip_address = resource.Body('ipv6_vip_address')
    #: IPv6 vip subnet id
    ipv6_vip_subnet_id = resource.Body('ipv6_vip_virsubnet_id')
    #: IPv6 vip port id
    ipv6_vip_port_id = resource.Body('ipv6_vip_port_id')
