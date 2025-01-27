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


class FunctionInvocation(resource.Resource):
    base_path = '/fgs/functions/%(func_urn)s'
    # Capabilities
    allow_create = True

    _query_mapping = resource.QueryParameters('func_urn')

    # Properties
    func_urn = resource.URI('func_urn', type=str)

    # Attributes
    invoke_summary = resource.Header('X-Cff-Invoke-Summary', type=str)
    cff_request_id = resource.Header('X-Cff-Request-Id', type=str)
    request_id = resource.Body('request-id', type=str)
    function_log = resource.Header('X-Cff-Function-Log', type=str)
    billing_duration = resource.Header('X-CFF-Billing-Duration', type=str)
    response_version = resource.Header('X-Cff-Response-Version', type=str)
    err_code = resource.Header('X-Func-Err-Code', type=str)
    err = resource.Header('X-Is-Func-Err', type=str)

    def _invocation(self, session, action, attrs: dict):
        """Function Execution
        """
        url = (self.base_path % self._uri.attributes) + f'/{action}'
        response = session.post(url, json=str(attrs).replace("'", '"'))
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self
