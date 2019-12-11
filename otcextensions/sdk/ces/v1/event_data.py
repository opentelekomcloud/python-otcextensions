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


class DatapointsSpec(resource.Resource):

    # Properties
    # time of the metric collection
    timestamp = resource.Body('timestamp')
    # Indicates the event type e.g. instance_host_info
    typespec = resource.Body('type')
    # host configuration information
    value = resource.Body('value')


class EventData(resource.Resource):

    base_path = '/event-data'

    # capabilities
    allow_list = True
    # allow_create = True

    _query_mapping = resource.QueryParameters(
        'dim', 'from', 'to', 'namespace', 'type'
    )

    # Properties
    # Datapoints retrieve the metrics data list
    datapoints = resource.Body('datapoints', type=list,
                               list_type=DatapointsSpec)
