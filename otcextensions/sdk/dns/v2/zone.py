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
from openstack.dns.v2 import zone
from openstack import utils

from otcextensions.sdk.dns.v2 import _base


class Router(_base.Resource):
    """DNS Private Zone Router Resource"""
    router_id = resource.Body('router_id')
    router_region = resource.Body('router_region')
    status = resource.Body('status')


class Zone(zone.Zone):
    """DNS ZONE Resource"""

    _query_mapping = resource.QueryParameters(
        'name', 'type', 'email', 'status', 'description', 'ttl',
        'limit', 'marker', 'router', 'zone_type'
    )

    #: Recordset number of the zone
    record_num = resource.Body('record_num', type=int)
    #: A dictionary represent Router(VPC), for private zone
    router = resource.Body('router', type=Router)
    #: Router list associated to this zone
    routers = resource.Body('routers', type=list, list_type=Router)
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
        return self._action(session, 'associaterouter', body)

    def disassociate_router(self, session, **router):
        body = {'router': {}}
        body['router']['router_id'] = router.get('router_id')
        if 'router_region' in router:
            body['router']['router_region'] = router.get('router_region')
        return self._action(session, 'disassociaterouter', body)
