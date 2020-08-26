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
    # Metric Value, the value is the same as that of
    # parameter filter
    average = resource.Body('average')
    maximum = resource.Body('max')
    minimum = resource.Body('min')
    sumspec = resource.Body('sum')
    variance = resource.Body('variance')
    # time of the metric collection
    timestamp = resource.Body('timestamp')
    # indicates the metric unit
    unit = resource.Body('unit')


class MetricData(resource.Resource):

    resource_key = ''
    resources_key = ''
    base_path = '/metric-data'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'namespace', 'period', 'filter', 'metric_name', 'dim.0', 'from',
        'to')

    # Properties
    # Datapoints retrieve the metrics data list
    datapoints = resource.Body('datapoints', type=list,
                               list_type=DatapointsSpec)
    # Metric Name like 'cpu_util'
    metric_name = resource.Body('metric_name')
