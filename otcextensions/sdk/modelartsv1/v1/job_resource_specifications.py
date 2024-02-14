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
#
from openstack import resource


class JobResourceSpecifications(resource.Resource):
    base_path = "job/resource-specs"
    resources_key = "specs"

    allow_list = True
    allow_fetch = True
    allow_patch = True

    #: Job type
    job_type = resource.Body("job_type", type=str)

    #: Engine ID of a job
    engine_id = resource.Body("engine_id", type=int)

    #: Project type
    project_type = resource.Body("project_type", type=int)

    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)

    #: Error message of a failed API call
    error_message = resource.Body("error_message", type=str)

    #: Error code of a failed API call
    error_code = resource.Body("error_code", type=str)

    #: Total number of job resource specifications
    spec_total_count = resource.Body("spec_total_count", type=int)

    #: List of resource specifications attributes
    specs = resource.Body("specs", type=list)
