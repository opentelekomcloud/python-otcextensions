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


class Alias(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/aliases'
    resources_key = ''

    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True
    allow_commit = True

    # Properties
    function_urn = resource.URI('function_urn', type=str)
    name = resource.Body('name', type=str, alternate_id=True)
    version = resource.Body('version', type=str)
    description = resource.Body('description', type=str)
    additional_version_weights = resource.Body(
        'additional_version_weights', type=dict
    )
    additional_version_strategy = resource.Body(
        'additional_version_strategy', type=dict
    )

    # Attributes
    last_modified = resource.Body('last_modified', type=str)
    alias_urn = resource.Body('alias_urn', type=str)

    def _update_alias(self, session, function, alias, **attrs):
        """Update Function Alias
        """
        urn = function.func_urn.rpartition(':')[0]
        url = self.base_path % {'function_urn': urn} + f'/{alias.id}'
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
