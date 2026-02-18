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


class DownlinkVpc(resource.Resource):
    #: Specifies the ID of the VPC where the private NAT gateway works.
    vpc_id = resource.Body('vpc_id')

    #: Specifies the ID of the subnet where the private NAT gateway works.
    virsubnet_id = resource.Body('virsubnet_id')

    #: Specifies the private IP address of the private NAT gateway.
    ngport_ip_address = resource.Body('ngport_ip_address')


class Tag(resource.Resource):
    #: Specifies the tag key. Up to 128 Unicode characters. Cannot be blank.
    key = resource.Body('key')

    #: Specifies the tag value. Up to 255 Unicode characters.
    value = resource.Body('value')


class PrivateNatGateway(resource.Resource):
    resources_key = 'gateways'
    resource_key = 'gateway'
    base_path = '/v3/%(project_id)s/private-nat/gateways'

    allow_list = True

    _query_mapping = resource.QueryParameters(
        'description',
        'enterprise_project_id',
        'id',
        'limit',
        'marker',
        'name',
        'page_reverse',
        'project_id',
        'spec',
        'status',
        'virsubnet_id',
        'vpc_id',
    )

    # Properties
    #: Specifies the time when the private NAT gateway was created.
    #: It is a UTC time in yyyy-mm-ddThh:mm:ssZ format.
    created_at = resource.Body('created_at')
    #: Provides supplementary information about the private NAT gateway.
    #: The description can contain up to 255 characters.
    #:  Cannot contain angle brackets (<>).
    description = resource.Body('description')
    #: Specifies the VPC where the private NAT gateway works.
    #: Each item contains:
    #: * vpc_id: Specifies the ID of the VPC.
    #: * virsubnet_id: Specifies the ID of the subnet.
    #: * ngport_ip_address: Specifies the private IP address of the gateway.
    downlink_vpcs = resource.Body('downlink_vpcs', type=list,
                                  list_type=DownlinkVpc)
    #: Specifies the ID of the enterprise project that is associated
    #: with the private NAT gateway when the private NAT gateway is created.
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Specifies the private NAT gateway ID.
    id = resource.Body('id')
    #: Specifies the private NAT gateway name.
    name = resource.Body('name')
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the maximum number of rules.
    #: Value range: 0–65535.
    rule_max = resource.Body('rule_max', type=int)
    #: Specifies the private NAT gateway specifications.
    #: Enumeration values:
    #: * Small (default)
    #: * Medium
    #: * Large
    #: * Extra-large
    spec = resource.Body('spec')
    #: Specifies the private NAT gateway status.
    #: Enumeration values:
    #: * ACTIVE: The private NAT gateway is running properly.
    #: * FROZEN: The private NAT gateway is frozen.
    status = resource.Body('status')
    #: Specifies the list of tags.
    #: Each tag contains:
    #: * key: Specifies the tag key. Up to 128 Unicode characters.
    #: * value: Specifies the tag value. Up to 255 Unicode characters.
    tags = resource.Body('tags', type=list, list_type=Tag)
    #: Specifies the maximum number of transit IP addresses
    #: in a transit IP address pool.
    #: Value range: 1–100.
    transit_ip_pool_size_max = resource.Body('transit_ip_pool_size_max',
                                             type=int)
    #: Specifies the time when the private NAT gateway was updated.
    #: It is a UTC time in yyyy-mm-ddThh:mm:ssZ format.
    updated_at = resource.Body('updated_at')


class PageInfo(resource.Resource):
    next_marker = resource.Body('next_marker')
    previous_marker = resource.Body('previous_marker')
    current_count = resource.Body('current_count', type=int)
