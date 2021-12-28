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


class ExtraDHCPOpt(resource.Resource):
    #: Specifies the NTP server address configured for the subnet.
    opt_value = resource.Body('opt_value')
    #: Specifies the NTP server address name configured for the subnet.
    #: Currently, the value can only be set to ntp.
    opt_name = resource.Body('opt_name', default='ntp')


class Subnet(resource.Resource):
    resource_key = 'subnet'
    resources_key = 'subnets'
    base_path = '/v1/%(project_id)s/subnets'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters('vpc_id')

    # Properties
    project_id = resource.URI('project_id')
    description = resource.Body('description')
    #: Specifies the subnet CIDR block.
    cidr = resource.Body('cidr')
    #: Specifies the gateway of the subnet.
    gateway_ip = resource.Body('gateway_ip')
    #: Specifies whether DHCP is enabled for the subnet.
    dhcp_enable = resource.Body('dhcp_enable')
    #: Specifies the IP address of DNS server 1 on the subnet.
    primary_dns = resource.Body('primary_dns')
    #: Specifies the IP address of DNS server 2 on the subnet.
    secondary_dns = resource.Body('secondary_dns')
    #: Specifies the DNS server address list of a subnet.
    #: This field is required if use more than two DNS servers.
    dns_list = resource.Body('dnsList', type=list, list_type=str)
    #: Specifies the AZ to which the subnet belongs
    availability_zone = resource.Body('availability_zone')
    #: Specifies the ID of the VPC to which the subnet belongs.
    vpc_id = resource.Body('vpc_id')
    #: Specifies the NTP server address configured for the subnet.
    extra_dhcp_opts = resource.Body('extra_dhcp_opts', type=list,
                                    list_type=ExtraDHCPOpt)

    status = resource.Body('status')
    neutron_network_id = resource.Body('neutron_network_id')
    neutron_subnet_id = resource.Body('neutron_subnet_id')


def vpc_subnet_base_path(vpc_id):
    """Special case of subnet resource path"""
    return f'/v1/%(project_id)s/vpcs/{vpc_id}/subnets'
