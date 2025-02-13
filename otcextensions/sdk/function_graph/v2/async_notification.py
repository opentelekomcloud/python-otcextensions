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


class FuncDestinationConfig(resource.Resource):
    # Object type.
    # OBS
    # SMN
    # FunctionGraph
    destination = resource.Body('destination', type=str)
    # Parameters (in JSON format) corresponding to the target service.
    param = resource.Body('param', type=str)


class FuncAsyncDestinationConfig(resource.Resource):
    on_success = resource.Body('on_success', type=FuncDestinationConfig)
    on_failure = resource.Body('on_failure', type=FuncDestinationConfig)


class Notification(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/async-invoke-config'
    # Capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True
    allow_commit = True

    create_method = 'PUT'

    create_requires_id = False
    requires_id = False

    _query_mapping = resource.QueryParameters(
        'marker', 'limit',
    )
    # Properties
    function_urn = resource.URI('function_urn', type=str)

    # Attributes
    # Function URN.
    func_urn = resource.Body('func_urn', type=str)
    # Maximum validity period of a message. Value range: 1-86,400. Unit: second.
    max_async_event_age_in_seconds = resource.Body(
        'max_async_event_age_in_seconds', type=int
    )
    max_async_retry_attempts = resource.Body(
        'max_async_retry_attempts', type=int
    )
    # Asynchronous invocation target.
    destination_config = resource.Body(
        'destination_config', type=FuncAsyncDestinationConfig
    )
    # Time when asynchronous execution notification was configured.
    created_at = resource.Body('created_time', type=str)
    # Time when the asynchronous execution notification settings were last modified.
    updated_at = resource.Body('last_modified', type=str)
    # Whether to enable asynchronous invocation status persistence.
    enable_async_status_log = resource.Body(
        'enable_async_status_log', type=str
    )


class Requests(resource.Resource):
    base_path = '/fgs/functions/%(function_urn)s/async-invocations'
    resources_key = 'invocations'

    _query_mapping = resource.QueryParameters(
        'request_id', 'marker', 'limit',
        'status', 'query_begin_time', 'query_end_time'
    )

    # Capabilities
    allow_list = True
    allow_create = True

    # Properties
    function_urn = resource.URI('function_urn', type=str)
    # Stop mode.
    # Enumeration values:
    # force
    # recursive
    type = resource.Body('type', type=str)

    # Attributes
    # Asynchronous invocation request ID.
    request_id = resource.Body('request_id', type=str)
    # Asynchronous invocation status. Options:
    # WAIT
    # RUNNING
    # SUCCESS
    # FAIL
    # DISCARD
    status = resource.Body('status', type=str)
    # Asynchronous invocation error information.
    # If the execution is successful, no value is returned.
    error_message = resource.Body('error_message', type=str)
    # Asynchronous invocation error code.
    # If the execution is successful, 0 is returned.
    error_code = resource.Body('error_code', type=int)
    # Start time of the asynchronous invocation.
    # The format is "YYYY-MM-DD'T'HH:mm:ss" (UTC time).
    start_time = resource.Body('start_time', type=str)
    # End time of the asynchronous invocation.
    # The format is "YYYY-MM-DD'T'HH:mm:ss" (UTC time).
    end_time = resource.Body('end_time', type=str)

    def _stop(self, session, function_urn, **attrs):
        """Stop asynchronous invocation of a function
        """
        url = ('fgs/functions/%(function_urn)s/cancel' %
               {'function_urn': function_urn})
        response = session.post(url, json=attrs)
        exceptions.raise_from_response(response)
