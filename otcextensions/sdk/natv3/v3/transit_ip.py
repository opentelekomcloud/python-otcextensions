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


class TransitIpTag(resource.Resource):
    key = resource.Body("key")
    value = resource.Body("value")


class PrivateTransitIp(resource.Resource):
    resources_key = "transit_ips"
    resource_key = "transit_ip"
    base_path = "/private-nat/transit-ips"

    # capabilities
    allow_list = True
    allow_fetch = True
    allow_create = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        "limit",
        "marker",
        "page_reverse",
        "id",
        "project_id",
        "network_interface_id",
        "ip_address",
        "virsubnet_id",
        "transit_subnet_id",
        "gateway_id",
        "enterprise_project_id",
        "description",
    )

    #: Specifies the transit IP address ID.
    id = resource.Body("id")

    #: Specifies the project ID.
    project_id = resource.Body("project_id")

    #: Specifies the network interface ID.
    network_interface_id = resource.Body("network_interface_id")

    #: Specifies the transit IP address.
    ip_address = resource.Body("ip_address")

    #: Specifies the private NAT gateway ID.
    gateway_id = resource.Body("gateway_id")

    #: Specifies when the transit IP address was created.
    created_at = resource.Body("created_at")

    #: Specifies when the transit IP address was updated.
    updated_at = resource.Body("updated_at")

    #: Specifies the transit IP address tags.
    tags = resource.Body("tags", type=list, list_type=TransitIpTag)

    #: Specifies the subnet ID of the current VPC.
    virsubnet_id = resource.Body("virsubnet_id")

    #: Specifies the transit IP address status.
    #: ACTIVE, FROZEN, INACTIVE
    status = resource.Body("status")

    #: Specifies the enterprise project ID.
    enterprise_project_id = resource.Body("enterprise_project_id")
