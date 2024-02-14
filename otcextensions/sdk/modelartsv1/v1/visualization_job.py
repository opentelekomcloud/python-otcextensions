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
from otcextensions.sdk.modelartsv1.v1 import _base


class VisualizationJob(resource.Resource):
    base_path = "/visualization-jobs"
    resources_key = "jobs"

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True

    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Error message of a failed API call. This parameter is not
    #:  included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=str)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=str)
    #: ID of a training job
    job_id = resource.Body("job_id", type=int)
    #: Name of a training job
    job_name = resource.Body("job_name", type=str)
    #: Timestamp when a training job is created
    created_at = resource.Body("create_time", type=float)

    #: Total number of the queried visualization jobs
    job_total_count = resource.Body("job_total_count", type=int)
    #: Number of visualization jobs that can be created
    job_count_limit = resource.Body("job_count_limit", type=int)
    #: Visualization job attributes
    # jobs = resource.Body('jobs', type=str) #type=list, list_type=Job)
    jobs = resource.Body("jobs", type=list, list_type=dict)
    #: Maximum number of training jobs
    quotas = resource.Body("quotas", type=int)
    #: Charged resource ID of a visualization job
    resource_id = resource.Body("resource_id", type=str)
    #: Endpoint of a visualization job
    service_url = resource.Body("service_url", type=str)
    #: Auto stop duration. The value ranges from 0 to 2
    duration = resource.Body("duration", type=int)
    #: Description of a visualization job
    job_desc = resource.Body("job_desc", type=str)
    #: Remaining auto stop duration
    remaining_duration = resource.Body("remaining_duration", type=float)
    #: Status of a visualization job. For details about the job statuses,
    #:  see Job Statuses.
    status = resource.Body("status", type=int)
    #: Path for storing visualization job logs
    train_url = resource.Body("train_url", type=str)


class VisualizationJobStop(resource.Resource):
    base_path = "/visualization-jobs/{job_id}/stop"
    jobId = resource.URI("jobId")


class VisualizationJobRestart(resource.Resource):
    base_path = "/visualization-jobs/{job_id}/restart"
    jobId = resource.URI("jobId")
