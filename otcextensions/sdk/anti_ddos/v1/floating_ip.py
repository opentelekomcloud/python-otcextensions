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
from openstack import _log

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class FloatingIP(sdk_resource.Resource):

    resources_key = 'ddosStatus'
    base_path = '/antiddos'

    # capabilities
    allow_list = True
    allow_get = True
    allow_delete = True
    allow_update = True

    _query_mapping = resource.QueryParameters('status',
                                              'limit',
                                              'offset',
                                              'ip')

    # Properties
    floating_ip_id = resource.Body('floating_ip_id', alternate_id=True)
    #: Floating ipaddress
    floating_ip_address = resource.Body('floating_ip_address')
    #: Flag to indicate whether L7 protection is enabled
    #: *Type: bool*
    is_enable_l7 = resource.Body('enable_L7', type=bool)
    #: Traffic segment id
    #: Valid values are from `1` to `9`
    #: *Type: int*
    traffic_pos_id = resource.Body('traffic_pos_id', type=int)
    #: Http request segment id
    #: Valid values are from `1` to `15`
    #: *Type: int*
    http_request_pos_id = resource.Body('http_request_pos_id', type=int)
    #: Cleaning access limit id
    #: Valid values are from `1` to `8`
    #: *Type: int*
    cleaning_access_pos_id = resource.Body('cleaning_access_pos_id', type=int)
    #: Application type id
    #: Valid values are from `0`, `1`
    #: *Type: int*
    app_type_id = resource.Body('app_type_id', type=int)

    #: Network type: EIP or ELB
    network_type = resource.Body('network_type')
    #: Status of the EIP
    #: Possible values:
    #: * `normal`: indicates that the defense status is normal.
    #: * `configging`: indicates that defense is being configured.
    #: * `notConfig`: indicates that defense is not configured.
    #: * `packetcleaning`: indicates that traffic cleaning is underway.
    #: * `packetdropping`: indicates that traffic is discarded.
    #: *Type: str*
    status = resource.Body('status')
    #: Task id
    task_id = resource.Body('task_id')

    def update(self, session, prepend_key=True, has_body=True):
        # floating update requires body to have `enable_L7, traffic_pos_id
        # http_request_pos_id, cleaning_access_pos_id, app_type_id`
        # so enforce them dirty

        self._body._dirty.add('enable_L7')
        self._body._dirty.add('traffic_pos_id')
        self._body._dirty.add('http_request_pos_id')
        self._body._dirty.add('cleaning_access_pos_id')
        self._body._dirty.add('app_type_id')

        return super(FloatingIP, self).update(
            session,
            prepend_key=prepend_key,
            has_body=has_body)
