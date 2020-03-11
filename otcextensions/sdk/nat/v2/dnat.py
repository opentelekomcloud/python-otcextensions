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


class Dnat(resource.Resource):
    resources_key = 'dnat_rules'
    resource_key = 'dnat_rule'
    base_path = '/dnat_rules'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'admin_state_up', 'cidr', 'created_at', 'external_service_port',
        'floating_ip_address', 'floating_ip_id', 'id',
        'internal_service_port', 'limit', 'nat_gateway_id', 'network_id',
        'port_id', 'private_ip', 'protocol', 'source_type', 'status',
        'tenant_id'
    )

    # Properties
    #: Specifies whether DNAT rule is enabled / disabled
    #: *true:* DNAT rule is enabled
    #: *false:* DNAT rule is disabled
    admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies when the rule is created.
    #: The format is yyyy-mm-dd hh:mm:ss.
    created_at = resource.Body('created_at')
    #: Specifies the port for providing external services.
    external_service_port = resource.Body('external_service_port', type=int)
    #: Specifies the EIP
    floating_ip_address = resource.Body('floating_ip_address')
    #: Specifies the EIP ID
    floating_ip_id = resource.Body('floating_ip_id')
    #: Specifies the gateway ID.
    gateway_id = resource.Body('gateway_id')
    #: Specifies the ID of the DNAT rule.
    id = resource.Body('id')
    #: Specifies port used by ECS/BMS to provide services for external systems
    internal_service_port = resource.Body('internal_service_port', type=int)
    #: Specifies the ID of the NAT gateway.
    nat_gateway_id = resource.Body('nat_gateway_id')
    #: Specifies the port ID of an ECS or BMS
    #: Parameter is used in the VPC scenario.
    #: This parameter is an alternative to private_ip
    port_id = resource.Body('port_id')
    #: Specifies the IP address of a Direct Connect connection.
    #: Parameter is used in the Direct Connect scenario.
    #: This parameter is an alternative to port_id.
    private_ip = resource.Body('private_ip')
    #: Specifies the project ID.
    project_id = resource.Body('tenant_id')
    #: Specifies the protocol type. Currently TCP(6), UDP(17) and ANY(0)
    protocol = resource.Body('protocol')
    #: Specifies the status of the DNAT rule
    status = resource.Body('status')
