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


class ResponseInfoHeaderSpec(resource.Resource):
    key = resource.Body('key', type=str)
    value = resource.Body('value', type=str)


class ErrorResponse(resource.Resource):
    # Properties
    gateway_id = resource.URI('gateway_id')
    group_id = resource.URI('group_id')
    response_id = resource.URI('response_id')
    response_type = resource.URI('response_type')

    status = resource.Body('status', type=int)
    body = resource.Body('body', type=str)
    headers = resource.Body('headers', type=list,
                            list_type=ResponseInfoHeaderSpec)
    auth_failure = resource.Body('AUTH_FAILURE')
    auth_header_missing = resource.Body('AUTH_HEADER_MISSING')
    authorizer_failure = resource.Body('AUTHORIZER_FAILURE')
    authorizer_conf_failure = resource.Body('AUTHORIZER_CONF_FAILURE')
    authorizer_identities_failure = (
        resource.Body('AUTHORIZER_IDENTITIES_FAILURE'))
    backend_unavailable = resource.Body('BACKEND_UNAVAILABLE')
    backend_timeout = resource.Body('BACKEND_TIMEOUT')
    throttled = resource.Body('THROTTLED')
    unauthorized = resource.Body('UNAUTHORIZED')
    access_denied = resource.Body('ACCESS_DENIED')
    not_found = resource.Body('NOT_FOUND')
    request_parameters_failure = resource.Body('REQUEST_PARAMETERS_FAILURE')
    default_4xx = resource.Body('DEFAULT_4XX')
    default_5xx = resource.Body('DEFAULT_5XX')
    third_auth_failure = resource.Body('THIRD_AUTH_FAILURE')
    third_auth_identities_failure = (
        resource.Body('THIRD_AUTH_IDENTITIES_FAILURE'))
    third_auth_conf_failure = resource.Body('THIRD_AUTH_CONF_FAILURE')
    orchestration_parameter_not_found = (
        resource.Body('ORCHESTRATION_PARAMETER_NOT_FOUND'))
    orchestration_failure = resource.Body('ORCHESTRATION_FAILURE')

    def _get(self, session, gateway_id, group_id, response_id,
             response_type,):
        url = (f'/apigw/instances/{gateway_id}/api-groups/{group_id}/'
               f'gateway-responses/{response_id}/{response_type}')
        response = session.get(url)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _update(self, session, gateway_id, group_id, response_id,
                response_type, **attrs):
        url = (f'/apigw/instances/{gateway_id}/api-groups/{group_id}/'
               f'gateway-responses/{response_id}/{response_type}')
        """Update the resource with the given attributes."""
        response = session.put(url, json=attrs)
        exceptions.raise_from_response(response)
        self._translate_response(response)
        return self

    def _delete(self, session, gateway_id, group_id, response_id,
                response_type,):
        url = (f'/apigw/instances/{gateway_id}/api-groups/{group_id}/'
               f'gateway-responses/{response_id}/{response_type}')
        """Delete the resource."""
        response = session.delete(url)
        exceptions.raise_from_response(response)
        return None
