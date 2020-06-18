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

from otcextensions.sdk.vpc.v2 import _base


class Peering(_base.Resource):
    resources_key = 'peerings'
    resource_key = 'peering'
    base_path = '/vpc/peerings'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'id', 'marker', 'limit', 'name', 'router_id',
        'status', 'project_id', project_id='tenant_id',
        router_id='vpc_id'
    )

    #: Specifies the VPC peering connection ID.
    #: *Type: uuid*
    id = resource.Body('id')
    #: Specifies information about the local VPC.
    #: *Type: dict*
    accept_vpc_info = resource.Body('accept_vpc_info', type=dict)
    #: Specifies information about the local VPC.
    #: *Type: dict*
    request_vpc_info = resource.Body('request_vpc_info', type=dict)
    #: Specifies the name of the VPC peering connection.
    name = resource.Body('name')
    #: Specifies the status.
    status = resource.Body('status')
    #: Provides supplementary information about the VPC peering connection.
    description = resource.Body('description')
    #: Specifies the time (UTC) when the VPC peering connection is created.
    #:  Format is *yyyy-mm-dd hh:mm:ss*.
    created_at = resource.Body('created_at')
    #: Specifies the time (UTC) when the VPC peering connection is updated.
    #:  Format is *yyyy-mm-dd hh:mm:ss*.
    updated_at = resource.Body('updated_at')

    def _set_peering(self, session, set_status):
        """Accept/Reject Peering Request"""
        url = utils.urljoin(self.base_path, self.id, set_status)
        response = session.put(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
