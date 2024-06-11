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


class AsyncJob(resource.Resource):
    resource_key = 'async_job'
    base_path = '/jobs'

    allow_fetch = True
    requires_id = False

    project_id = resource.Body('project_id')
    job_id = resource.Body('job_id')
    status = resource.Body('status')
    job_type = resource.Body('job_type')
    begin_time = resource.Body('begin_time')
    end_time = resource.Body('end_time')
    error_code = resource.Body('error_code')
    fail_reason = resource.Body('fail_reason')
    entities = resource.Body('entities', type=list)
