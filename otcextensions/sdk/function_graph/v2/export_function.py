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
import urllib

from openstack import resource
from openstack import exceptions


class Export(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/export'

    # Capabilities
    allow_fetch = True

    _query_mapping = resource.QueryParameters(
        'config', 'code', 'type'
    )

    # Properties
    function_urn = resource.URI('function_urn', type=str)

    # Attributes
    file_name = resource.Body('file_name', type=str)
    code_url = resource.Body('code_url', type=str)

    def _export(self, session, function, **query):
        """Export a function
        """
        query_params = urllib.parse.urlencode(query)
        urn = function.func_urn.rpartition(":")[0]
        url = self.base_path % {'function_urn': urn}
        url += '?' + query_params
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
