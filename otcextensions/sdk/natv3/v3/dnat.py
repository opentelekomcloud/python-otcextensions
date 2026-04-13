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


class PrivateDnat(resource.Resource):
    resources_key = "dnat_rules"
    resource_key = "dnat_rule"
    base_path = "/private-nat/dnat-rules"

    # capabilities
    allow_create = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        "limit",
        "marker",
        "page_reverse",
        "id",
        "project_id",
        "enterprise_project_id",
        "description",
        "gateway_id",
        "transit_ip_id",
        "external_ip_address",
        "network_interface_id",
        "type",
        "private_ip_address",
        "protocol",
        "internal_service_port",
        "transit_service_port",
        "created_at",
        "updated_at",
    )

    # Properties returned by the API and/or accepted on create

    #: Specifies the DNAT rule ID.
    id = resource.Body("id")

    #: Specifies the project ID.
    project_id = resource.Body("project_id")

    #: Provides supplementary information about the DNAT rule.
    description = resource.Body("description")

    #: Specifies the ID of the transit IP address.
    transit_ip_id = resource.Body("transit_ip_id")

    #: Specifies the private NAT gateway ID.
    gateway_id = resource.Body("gateway_id")

    #: Specifies the network interface ID.
    network_interface_id = resource.Body("network_interface_id")

    #: Specifies the backend resource type of the DNAT rule.
    #: COMPUTE, VIP, ELB, ELBv3, CUSTOMIZE
    type = resource.Body("type")

    #: Specifies the protocol type.
    #: tcp, udp, any
    protocol = resource.Body("protocol")

    #: Specifies the port IP address that the NAT gateway uses.
    private_ip_address = resource.Body("private_ip_address")

    #: Specifies the backend resource port number.
    internal_service_port = resource.Body("internal_service_port", type=int)

    #: Specifies the transit IP port number.
    transit_service_port = resource.Body("transit_service_port", type=int)

    #: Specifies the enterprise project ID associated with the DNAT rule.
    enterprise_project_id = resource.Body("enterprise_project_id")

    #: Specifies the DNAT rule status.
    #: ACTIVE, FROZEN
    status = resource.Body("status")

    #: Specifies when the DNAT rule was created.
    created_at = resource.Body("created_at")

    #: Specifies when the DNAT rule was updated.
    updated_at = resource.Body("updated_at")
