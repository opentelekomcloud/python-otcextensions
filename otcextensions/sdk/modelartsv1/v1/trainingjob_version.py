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


class GetLogfileName(resource.Resource):
    base_path = (
        "/training-jobs/%(jobId)s/versions/%(versionId)s/log/file-names"
    )

    # resources_key = "versions"
    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: ID of a training job
    jobId = resource.URI("jobId", type=int)
    #: Version ID of a training job
    versionId = resource.URI("versionId", type=int)


class TrainingJobVersionLogs(resource.Resource):
    base_path = "/training-jobs/%(jobId)s/versions/%(versionId)s/aom-log"

    resources_key = "versions"
    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    config = resource.Body("config", type=dict)

    #: Status of a training job. For details about the job statuses,
    #:  see Job Statuses.
    status = resource.Body("status", type=int)
    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Error message of a failed API call. This parameter is not included
    #:  when the API call succeeds.
    error_msg = resource.Body("error_msg", type=bool)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=bool)
    #: ID of a training job
    jobId = resource.URI("jobId", type=int)
    # job_id = resource.URI('job_id', type=str)
    #: Name of a training job
    job_name = resource.Body("job_name", type=str)
    #: Version ID of a training job
    versionId = resource.URI("versionId", type=int)
    #: Timestamp when a training job is created


class TrainingJobVersion(resource.Resource):
    base_path = "/training-jobs/%(jobId)s/versions"

    resources_key = "versions"
    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    config = resource.Body("config", type=dict)

    #: Status of a training job. For details about the job statuses,
    #:  see Job Statuses.
    status = resource.Body("status", type=int)
    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Error message of a failed API call. This parameter is not included
    #:  when the API call succeeds.
    error_msg = resource.Body("error_msg", type=bool)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=bool)
    #: ID of a training job
    jobId = resource.URI("jobId", type=int)
    # job_id = resource.URI('job_id', type=str)
    #: Name of a training job
    job_name = resource.Body("job_name", type=str)
    #: Version ID of a training job
    version_id = resource.Body("versionId", type=int, alternate_id=True)
    #: Timestamp when a training job is created
    created_at = resource.Body("create_time", type=int)
    #: Charged resource ID of a training job
    resource_id = resource.Body("resource_id", type=str)
    #: Version name of a training job
    version_name = resource.Body("version_name", type=str)
    #: Description of a training job
    job_desc = resource.Body("job_desc", type=str)
    #: Number of versions of a training job
    version_count = resource.Body("version_count", type=int)
    #: Version parameters of a training job. For details,
    #:  see the sample response.
    versions = resource.Body("versions", type=list, list_type=dict)
    #: Total number of created jobs
    job_total_count = resource.Body("job_total_count", type=int)
    #: Number of training jobs that can be created
    job_count_limit = resource.Body("job_count_limit", type=int)
    #: Attributes of a training job.
    jobs = resource.Body("jobs", type=list, list_type=dict)
    quotas = resource.Body("quotas", type=str)
    pre_version_id = resource.Body("pre_version_id", type=int)
    engine_type = resource.Body("engine_type", type=int)
    engine_name = resource.Body("engine_name", type=str)
    engine_id = resource.Body("engine_id", type=int)
    engine_version = resource.Body("engine_version", type=str)
    app_url = resource.Body("app_url", type=str)
    boot_file_url = resource.Body("boot_file_url", type=str)
    parameter = resource.Body("parameter", type=list, list_type=dict)
    duration = resource.Body("duration", type=int)
    spec_id = resource.Body("spec_id", type=int)
    core = resource.Body("core", type=int)
    cpu = resource.Body("cpu", type=int)
    gpu_num = resource.Body("gpu_num", type=int)
    gpu_type = resource.Body("gpu_type", type=str)
    worker_server_num = resource.Body("worker_server_num", type=int)
    data_url = resource.Body("data_url", type=str)
    train_url = resource.Body("train_url", type=str)
    log_url = resource.Body("log_url", type=str)
    dataset_version_id = resource.Body("dataset_version_id", type=str)
    dataset_id = resource.Body("dataset_id", type=str)
    data_source = resource.Body("data_source", type=list, list_type=dict)
    user_image_url = resource.Body("user_image_url", type=str)
    user_command = resource.Body("user_command", type=str)
    model_id = resource.Body("model_id", type=int)
    model_metric_list = resource.Body("model_metric_list", type=str)
    system_metric_list = resource.Body("system_metric_list", type=str)
    dataset_name = resource.Body("dataset_name", type=str)
    dataset_version_name = resource.Body("dataset_version_name", type=str)
    spec_code = resource.Body("spec_code", type=str)
    start_time = resource.Body("start_time", type=int)
    volumes = resource.Body("volumes", type=list, list_type=dict)
    pool_id = resource.Body("pool_id", type=str)
    pool_name = resource.Body("pool_name", type=str)
    nas_mount_path = resource.Body("nas_mount_path", type=str)
    nas_share_addr = resource.Body("nas_share_addr", type=str)
    nas_type = resource.Body("nas_type", type=str)
