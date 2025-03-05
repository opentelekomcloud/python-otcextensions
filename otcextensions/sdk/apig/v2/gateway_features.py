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


class GatewayFeatures(resource.Resource):
    base_path = '/apigw/instances/%(gateway_id)s/features'
    resources_key = 'features'

    allow_list = True
    allow_create = True

    _query_mapping = resource.QueryParameters('limit', 'offset')

    # Properties
    gateway_id = resource.URI('gateway_id')
    # Feature name.
    name = resource.Body('name', type=str)
    # Indicates whether to enable the feature.
    enable = resource.Body('enable', type=bool)
    # Parameter configuration.
    config = resource.Body('config', type=str)

    # Attributes
    # Feature update time.
    updated_at = resource.Body('update_time')

    def _supported_features(self, session, gateway, **query):
        """List supported Gateway features.
        """
        query_params = self._query_mapping._transpose(query, GatewayFeatures)
        url = f'/apigw/instances/{gateway.id}/instance-features'
        response = session.get(url, params=query_params.copy())
        exceptions.raise_from_response(response)
        data = response.json()
        return data["features"]
