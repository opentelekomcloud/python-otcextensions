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
from openstack import _log
from openstack import resource
from openstack import utils

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.dns import dns_service

_logger = _log.setup_logging('openstack')


class Router(sdk_resource.Resource):
    """DNS Private Zone Router Resource"""
    router_id = resource.Body('router_id')
    router_region = resource.Body('router_region')
    status = resource.Body('status')


class Zone(sdk_resource.Resource):
    """DNS ZONE Resource"""
    resource_key = 'zone'
    resources_key = 'zones'
    base_path = '/zones'
    service = dns_service.DnsService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True
    update_method = "PATCH"

    _query_mapping = resource.QueryParameters(
        'zone_type', 'limit', 'marker', 'offset', 'tags',
        zone_type='type')

    #: Properties
    #: Timestamp when the zone was created
    created_at = resource.Body('created_at')
    #: Zone description
    #: *Type: str*
    description = resource.Body('description')
    #: The administrator email of this zone
    #: *Type: str*
    email = resource.Body('email')
    #: Links contains a `self` pertaining to this zone or a `next` pertaining
    #: to next page
    links = resource.Body('links', type=dict)
    #: The master list for slaver server to fetch DNS
    masters = resource.Body('masters', type=list)
    #: Zone name
    name = resource.Body('name')
    #: The pool which manages the zone, assigned by system
    pool_id = resource.Body('pool_id')
    #: The project id which the zone belongs to
    project_id = resource.Body('project_id')
    #: Recordset number of the zone
    record_num = resource.Body('record_num', type=int)
    #: A dictionary represent Router(VPC), for private zone
    router = resource.Body('router', type=Router)
    #: Router list associated to this zone
    routers = resource.Body('routers', type=list, list_type=Router)
    #: Serial number in the SOA record set in the zone,
    #: which identifies the change on the primary DNS server
    #: *Type: int*
    serial = resource.Body('serial', type=int)
    #: Zone status
    #: Valid values include `PENDING_CREATE`, `ACTIVE`,
    #: `PENDING_DELETE`, `ERROR`
    status = resource.Body('status')
    #: SOA TTL time, unit is seconds, default 300, TTL range 300-2147483647
    #: *Type: int*
    ttl = resource.Body('ttl', type=int)
    #: Timestamp when the zone was last updated
    updated_at = resource.Body('updated_at')
    #: Zone type, if private, domain will only available in a special VPC.
    #: Valid values include `private`, `public`
    #: *Type: str*
    zone_type = resource.Body('zone_type')

    def _action(self, session, action, body):
        """Preform actions given the message body.

        """
        url = utils.urljoin(self.base_path, self.id, action)
        return session.post(
            url,
            json=body)

    def associate_router(self, session, **router):
        body = {'router': {}}
        body['router']['router_id'] = router.get('router_id')
        if 'router_region' in router:
            body['router']['router_region'] = router.get('router_region')
        return self._action(session, 'accosiaterouter', body)

    def disassociate_router(self, session, **router):
        body = {'router': {}}
        body['router']['router_id'] = router.get('router_id')
        if 'router_region' in router:
            body['router']['router_region'] = router.get('router_region')
        return self._action(session, 'disaccosiaterouter', body)
