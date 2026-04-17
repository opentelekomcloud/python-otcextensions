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


class AssociatedTransitIp(resource.Resource):
    #: Specifies the transit IP address ID.
    transit_ip_id = resource.Body("transit_ip_id")

    #: Specifies the transit IP address.
    transit_ip_address = resource.Body("transit_ip_address")


class PrivateSnat(resource.Resource):
    resources_key = "snat_rules"
    resource_key = "snat_rule"
    base_path = "/private-nat/snat-rules"

    # capabilities
    allow_fetch = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        "limit",
        "marker",
        "page_reverse",
        "id",
        "project_id",
        "description",
        "gateway_id",
        "cidr",
        "virsubnet_id",
        "transit_ip_id",
        "transit_ip_address",
        "enterprise_project_id",
    )

    #: Specifies the SNAT rule ID.
    id = resource.Body("id")

    #: Specifies the project ID.
    project_id = resource.Body("project_id")

    #: Specifies the private NAT gateway ID.
    gateway_id = resource.Body("gateway_id")

    #: Specifies the CIDR block that matches the SNAT rule.
    cidr = resource.Body("cidr")

    #: Specifies the ID of the subnet that matches the SNAT rule.
    virsubnet_id = resource.Body("virsubnet_id")

    #: Provides supplementary information about the SNAT rule.
    description = resource.Body("description")

    #: Specifies the list of details of associated transit IP addresses.
    transit_ip_associations = resource.Body(
        "transit_ip_associations", type=list, list_type=AssociatedTransitIp
    )

    #: Specifies when the SNAT rule was created.
    created_at = resource.Body("created_at")

    #: Specifies when the SNAT rule was updated.
    updated_at = resource.Body("updated_at")

    #: Specifies the enterprise project ID.
    enterprise_project_id = resource.Body("enterprise_project_id")

    #: Specifies the SNAT rule status.
    #: ACTIVE, FROZEN
    status = resource.Body("status")
