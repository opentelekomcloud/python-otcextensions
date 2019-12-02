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


class DimensionsSpec(resource.Resource):

    # Properties
    #: dimension.name: object type e.g. ECS (instance_id)
    name = resource.Body('name')
    #: dimension.value: object id e.g. ECS ID
    value = resource.Body('value')


class Metric(resource.Resource):
    resource_key = 'metric'
    resources_key = 'metrics'
    base_path = '/metrics'

    # capabilities
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'dim', 'limit', 'metric_name', 'namespace', 'order', 'start'
    )

    # Properties
    #: List of metric dimensions
    #: dimension.name: object type e.g. ECS (instance_id)
    #: dimension.value: object id e.g. ECS ID
    dimensions = resource.Body('dimensions', type=list, list_type=DimensionsSpec)
    #: Shows the metric name
    metric_name = resource.Body('metric_name')
    #: Indicates the metric namespaces
    namespace = resource.Body('namespace')
    #: Indicates the metric unit
    unit = resource.Body('unit')


