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


class Config(resource.Resource):

    resources_key = 'redis_config'

    base_path = '/instances/%(instance_id)s/configs'

    # capabilities
    allow_list = True
    allow_commit = True
    commit_method = "PUT"

    # Properties
    #: Instance ID
    instance_id = resource.URI('instance_id')
    #: Parameter description
    description = resource.Body('description')
    #: Parameter default value
    default_value = resource.Body('default_value')
    #: Parameter ID
    id = resource.Body('param_id', alternate_id=True)
    #: Parameter Name
    name = resource.Body('param_name')
    #: Parameter value
    value = resource.Body('param_value')
    #: Parameter value range
    value_range = resource.Body('value_range')
    #: Parameter value type
    value_type = resource.Body('value_type')

    def _construct_dict_for_update(self, obj):
        return {
            key: obj[key] for key in ['param_id', 'param_value', 'param_name']
        }

    def _update(self, session, params):
        """Update parameters of the instance
        """
        filter_params = [
            self._construct_dict_for_update(obj) for obj in params
        ]
        body = {
            'redis_config': filter_params
        }
        uri = self.base_path % self._uri.attributes
        response = session.put(
            uri,
            json=body)
        return self._translate_response(response, False)
