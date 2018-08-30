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

from otcextensions.common import format
from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class TaskStatus(sdk_resource.Resource):

    base_path = '/query_task_status'

    # capabilities
    allow_get = True

    _query_mapping = resource.QueryParameters('task_id')

    # Properties
    #: Status of task
    #: validate status are `success`, `failed`, `waiting`, `running`
    task_status = resource.Body('task_status')
    #: Additional task status message
    task_msg = resource.Body('task_msg')


class FloatingIPStatus(sdk_resource.Resource):

    base_path = '/antiddos/%(floating_ip_id)s/status'

    # capabilities
    allow_get = True

    # Properties
    floating_ip_id = resource.URI('floating_ip_id')
    #: Status of Anti-DDos
    #: validate status are `normal`, `configging`, `notConfig`,
    #: `packetcleaning`, `packetdropping`
    status = resource.Body('status')


class FloatingIPLog(sdk_resource.Resource):

    resources_key = 'logs'
    base_path = '/antiddos/%(floating_ip_id)s/logs'

    _query_mapping = resource.QueryParameters('limit', 'offset', 'sort_dir')

    # capabilities
    allow_list = True

    # Properties
    #: start time
    #: *Type: int*
    start_time = resource.Body('start_time', type=format.TimeTMsStr)
    #: end time
    #: *Type: int*
    end_time = resource.Body('end_time', type=format.TimeTMsStr)
    #: Anti-ddos status
    #: *Type: int*
    status = resource.Body('status', type=int)
    #: Trigger bps (bit/s)
    #: *Type: int*
    trigger_bps = resource.Body('trigger_bps', type=int)
    #: Trigger package per second
    #: *Type: int*
    trigger_pps = resource.Body('trigger_pps', type=int)
    #: Trigger http requests
    #: *Type: int*
    trigger_http_pps = resource.Body('trigger_http_pps', type=int)


class FloatingIPDayStat(sdk_resource.Resource):

    resources_key = 'data'
    base_path = '/antiddos/%(floating_ip_id)s/daily'

    # capabilities
    allow_list = True

    # Properties
    #: Data start time
    #: *Type: int*
    period_start = resource.Body('period_start', type=format.TimeTMsStr)
    #: In (bit/s)
    #: *Type: int*
    bps_in = resource.Body('bps_in', type=int)
    #: Attack (bit/s)
    #: *Type: int*
    bps_attack = resource.Body('bps_attack', type=int)
    #: Total data (bit/s)
    #: *Type: int*
    total_bps = resource.Body('total_bps', type=int)
    #: Package in speed (/s)
    #: *Type: int*
    pps_in = resource.Body('pps_in', type=int)
    #: Package attack speed (/s)
    #: *Type: int*
    pps_attack = resource.Body('pps_attack', type=int)
    #: Total package speed (/s)
    #: *Type: int*
    total_pps = resource.Body('total_pps', type=int)


class FloatingIPWeekStatData(sdk_resource.Resource):
    # Properties
    #: Intercept time in one week
    #: *Type: int*
    ddos_intercept_times = resource.Body('ddos_intercept_times', type=int)
    #: *Type: int*
    ddos_blackhole_times = resource.Body('ddos_blackhole_times', type=int)
    #: *Type: int*
    max_attack_bps = resource.Body('max_attack_bps', type=int)
    #: *Type: int*
    max_attack_conns = resource.Body('max_attack_conns ', type=int)
    #: *Type: int*
    ddos_blackhole_times = resource.Body('ddos_blackhole_times', type=int)
    #: Data start time
    #: *Type: int*
    period_start_date = resource.Body('period_start_date',
                                      type=format.TimeTMsStr)


class FloatingIPWeekStat(sdk_resource.Resource):

    base_path = '/antiddos/weekly'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters('period_start_date')

    # Properties
    #: Intercept time in one week
    #: *Type: int*
    ddos_intercept_times = resource.Body('ddos_intercept_times', type=int)
    #: A list of data in one week
    #: *Type: list*
    weekdata = resource.Body('weekdata', type=list,
                             list_type=FloatingIPWeekStatData)
    #: Top 10 ip address in one week
    #: *Type: list*
    top10 = resource.Body('top10', type=list)
