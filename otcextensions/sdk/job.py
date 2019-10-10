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


class Job(resource.Resource):

    base_path = '/jobs'

    # capabilities
    allow_fetch = True

    # Properties
    #: id
    id = resource.Body('job_id', alternate_id=True)
    #: Additional sub information
    entities = resource.Body('entities', type=dict)
    #: Error code
    error_code = resource.Body('error_code')
    #: Fail reason
    fail_reason = resource.Body('fail_reason')
    #: Job finish time
    finish_time = resource.Body('end_time')
    #: Job start time
    start_time = resource.Body('begin_time')
    #: Status
    status = resource.Body('status')
    #: Job type
    #: *Type:str*
    type = resource.Body('job_type')


class JobProxyMixin(object):

    def wait_for_job(self, job_id, status='success',
                     failures=None, interval=2, wait=3600,
                     attribute='status'):
        failures = ['FAIL'] if failures is None else failures

        job = Job.existing(id=job_id).fetch(self)
        return resource.wait_for_status(
            self, job, status, failures, interval, wait, attribute='status'
        )
