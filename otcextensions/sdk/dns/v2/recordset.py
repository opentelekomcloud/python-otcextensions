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
# from openstack import exceptions
from openstack import resource

from otcextensions.sdk.dns.v2 import _base


class Recordset(_base.Resource):
    """DNS Recordset Resource"""
    resources_key = 'recordsets'
    base_path = '/zones/%(zone_id)s/recordsets'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'name', 'type', 'ttl', 'data', 'status', 'description',
        'limit', 'marker', 'offset', 'tags')

    #: Properties
    #: Timestamp when the zone was created
    created_at = resource.Body('create_at')
    #: Recordset description
    description = resource.Body('description')
    #: Is the recordset created by system.
    is_default = resource.Body('default', type=bool)
    #: Recordset name
    name = resource.Body('name')
    #: ID of the project which the recordset belongs to
    project_id = resource.Body('project_id')
    #: DNS record value list
    records = resource.Body('records', type=list)
    #: Recordset status
    #: Valid values include: `PENDING_CREATE`, `ACTIVE`,
    #: `PENDING_DELETE`, `ERROR`
    status = resource.Body('status')
    #: Time to live, default 300, available value 300-2147483647 (seconds)
    ttl = resource.Body('ttl', type=int)
    #: DNS type of the recordset
    #: Valid values include `A`, `AAA`, `MX`, `CNAME`, `TXT`, `NS`
    #: In private zones `SOA`, `SRV`, `PTR`
    type = resource.Body('type')
    #: Timestamp when the zone was last updated
    updated_at = resource.Body('update_at')
    #: The id of the Zone which this recordset belongs to
    zone_id = resource.URI('zone_id')
    #: The name of the Zone which this recordset belongs to
    zone_name = resource.Body('zone_name')
