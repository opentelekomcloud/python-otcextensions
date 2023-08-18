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


class HealthMonitor(resource.Resource):
    resource_key = 'healthmonitor'
    resources_key = 'healthmonitors'
    base_path = '/elb/healthmonitors'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'admin_state_up', 'delay', 'domain_name',
        'expected_codes', 'id', 'http_method',
        'max_retries', 'max_retries_down', 'monitor_port',
        'name', 'timeout', 'type', 'url_path',
        is_admin_state_up='admin_state_up',
    )

    # Properties
    #: Specifies the interval between health checks, in seconds.
    delay = resource.Body('delay', type=int)
    #: Specifies the domain name that HTTP requests are
    #: sent to during the health check.
    domain_name = resource.Body('domain_name')
    #: Specifies the expected HTTP status code.
    expected_codes = resource.Body('expected_codes')
    #: Specifies the HTTP method.
    http_method = resource.Body('http_method')
    #: Specifies the administrative status of the health check.
    is_admin_state_up = resource.Body('admin_state_up', type=bool)
    #: Specifies the number of consecutive health checks when
    #: the health check result of a backend server changes from
    #: OFFLINE to ONLINE.
    max_retries = resource.Body('max_retries', type=int)
    #: Specifies the number of consecutive health checks when
    #: the health check result of a backend server changes from
    #: ONLINE to OFFLINE
    max_retries_down = resource.Body('max_retries_down', type=int)
    #: Specifies the port used for the health check.
    monitor_port = resource.Body('monitor_port', type=int)
    #: Specifies the ID of the backend server group for which
    #: the health check is configured.
    pool_id = resource.Body('pool_id')
    #: Lists the IDs of backend server groups for which
    #: the health check is configured.
    pools = resource.Body('pools', type=list)
    #: Specifies the project ID.
    project_id = resource.Body('project_id')
    #: Specifies the maximum time required for waiting for a response
    #: from the health check, in seconds.
    timeout = resource.Body('timeout', type=int)
    #: Specifies the health check protocol.
    type = resource.Body('type')
    #: Specifies the HTTP request path for the health check.
    url_path = resource.Body('url_path')
    #: Specifies the time when the health check was configured.
    created_at = resource.Body('created_at')
    #: Specifies the time when the health check was updated.
    updated_at = resource.Body('updated_at')
