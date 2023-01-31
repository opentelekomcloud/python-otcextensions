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
from openstack import exceptions
from openstack import resource
from openstack import utils


class PublicIPInfo(resource.Resource):
    #: Properties
    #: Specifies the ID of the EIP that uses the bandwidth.
    publicip_id = resource.Body('publicip_id')
    #: Specifies the obtained EIP if only IPv4 EIPs are available.
    publicip_address = resource.Body('publicip_address')
    #: Specifies the EIP type.
    publicip_type = resource.Body('publicip_type', default='5_bgp')


class Bandwidth(resource.Resource):
    resources_key = 'bandwidths'
    resource_key = 'bandwidth'
    base_path = '/v2.0/%(project_id)s/bandwidths'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'project_id', project_id='tenant_id',
    )

    # Properties
    project_id = resource.URI('project_id')
    #: Specifies the bandwidth name.
    #: *Type: dict*
    name = resource.Body('name', type=str)
    #: Specifies the bandwidth size.
    #: *Type: dict*
    size = resource.Body('size', type=int)
    #: Specifies whether the bandwidth is shared or dedicated.
    share_type = resource.Body('share_type', type=str)
    #: Specifies the project ID.
    publicip_info = resource.Body('publicip_info', type=list, elements=PublicIPInfo)
    #: Specifies the bandwidth type.
    bandwidth_type = resource.Body('bandwidth_type', type=str, default='share')
    #: Specifies that the bandwidth is billed by bandwidth.
    charge_mode = resource.Body('charge_mode', type=str)
    #: Specifies the bill information.
    billing_info = resource.Body('billing_info', type=str)
    #: Specifies the enterprise project ID.
    enterprise_project_id = resource.Body('enterprise_project_id', type=str)
    #: Specifies the bandwidth status.
    status = resource.Body('status', type=str)
    #: Specifies the time (UTC) when the bandwidth is created.
    created_at = resource.Body('created_at', type=str)
    #: Specifies the time (UTC) when the bandwidth is updated.
    updated_at = resource.Body('updated_at', type=str)
