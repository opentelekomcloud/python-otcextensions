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


class ApiEnvironment(resource.Resource):
    base_path = f'/apigw/instances/%(gateway_id)s/envs'

    allow_list = True
    allow_create = True
    allow_commit = True
    allow_delete = True

    resources_key = 'envs'

    _query_mapping = resource.QueryParameters('limit', 'offset', 'name')

    gateway_id = resource.URI('gateway_id')
    name = resource.Body('name')
    remark = resource.Body('remark')

    create_time = resource.Body('create_time')
    id = resource.Body('id')

    def _update_env(self, session, gateway, **attrs):
        """Update environment.
        """
        url = f'/apigw/instances/{gateway.id}/envs/{self.id}'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
