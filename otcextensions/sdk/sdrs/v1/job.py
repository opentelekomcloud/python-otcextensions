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


class EntitySpecSub(resource.Body):
    #: Properties
    #: Protection group ID
    server_group_id = resource.Body('server_group_id')


class SubJob(resource.Body):
    #: Properties
    #: Task begin time
    begin_time = resource.Body('begin_time')
    #: Error status code
    code = resource.Body('code')
    #: Task end time
    end_time = resource.Body('end_time')
    #: Additional info on job
    entities = resource.Body('entities', type=EntitySpecSub)
    #: SDRS Error code
    error_code = resource.Body('error_code')
    #: Fail reason
    fail_reason = resource.Body('fail_reason')
    #: Job id
    job_id = resource.Body('job_id')
    #: Job type
    job_type = resource.Body('job_type')
    #: Error message
    message = resource.Body('message')
    #: Job status
    status = resource.Body('status')


class EntitySpec(resource.Resource):
    #: Properties
    #: Protection group ID
    server_group_id = resource.Body('server_group_id')
    #: Sub job information
    sub_jobs = resource.Body('sub_jobs', type=SubJob)


class Job(resource.Resource):
    """SDRS Job Resource"""
    base_path = '/jobs'

    # capabilities
    allow_fetch = True

    #: Properties
    #: Task begin time
    begin_time = resource.Body('begin_time')
    #: Error status code
    code = resource.Body('code')
    #: Task end time
    end_time = resource.Body('end_time')
    #: Additional info on job
    entities = resource.Body('entities', type=EntitySpec)
    #: SDRS Error code
    error_code = resource.Body('error_code')
    #: Fail reason
    fail_reason = resource.Body('fail_reason')
    #: Job id
    job_id = resource.Body('job_id')
    #: Job type
    job_type = resource.Body('job_type')
    #: Error message
    message = resource.Body('message')
    #: Job status
    status = resource.Body('status')
