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
from openstack import exceptions


class MetricData(resource.Resource):
    base_path = '/apigw/instances/%(gateway_id)s/metric-data'
    resources_key = 'datapoints'
    _query_mapping = resource.QueryParameters('dim', 'metric_name', 'from',
                                              'to', 'period', 'filter')
    allow_list = True

    gateway_id = resource.URI('gateway_id')
    average = resource.Body('average', type=int)
    max = resource.Body('max', type=int)
    min = resource.Body('min', type=int)
    sum = resource.Body('sum', type=int)
    variance = resource.Body('variance', type=int)
    timestamp = resource.Body('timestamp')
    unit = resource.Body('unit')

    def get_metric_data(self, session, gateway_id, **params):
        """Retrieve metric data with the given parameters."""
        uri = f'apigw/instances/{gateway_id}/metric-data'
        response = session.get(uri, params=params)
        exceptions.raise_from_response(response)
        data = response.json()
        resources = data[self.resources_key]
        for raw_resource in resources:
            value = self.existing(
                connection=session._get_connection(),
                **raw_resource)
            yield value
