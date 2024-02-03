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


class TrainingJob(resource.Resource):
    base_path = "/training-jobs"

    resources_key = "jobs"

    allow_create = True
    allow_list = True
    allow_commit = False
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Status of a training job. For details about the job statuses,
    #:  see Job Statuses.
    status = resource.Body("status", type=bytes)
    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Error message of a failed API call. This parameter is not
    #:  included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=bool)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=bool)
    #: ID of a training job
    job_id = resource.Body("job_id", type=str, alternate_id=True)
    #: Name of a training job
    job_name = resource.Body("job_name", type=str)
    #: Version ID of a training job
    version_id = resource.Body("version_id", type=str)
    #: Timestamp when a training job is created
    #: Charged resource ID of a training job
    resource_id = resource.Body("resource_id", type=str)
    #: Version name of a training job
    version_name = resource.Body("version_name", type=str)
    status = resource.Body("status", type=str)
    #: Training job running duration, in milliseconds
    duration = resource.Body("duration", type=int)
    #: Total number of created jobs
    job_total_count = resource.Body("job_total_count", type=int)
    #: Number of training jobs that can be created
    job_count_limit = resource.Body("job_count_limit", type=int)
    #: Attributes of a training job.
    # jobs = resource.Body('jobs', type=list, list_type=Job)
    quotas = resource.Body("quotas", type=str)
    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Error message of a failed API call. This parameter is not
    #:  included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=bool)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=bool)
    #: Description of a training job
    job_desc = resource.Body("job_desc", type=str)
    #: Name of the previous version of a training job
    pre_version_id = resource.Body("pre_version_id", type=int)
    #: Model metrics of a training job. For details, see Table 5.
    model_metric_list = resource.Body("model_metric_list", type=str)
    #: System monitoring metrics of a training job. For details, see Table 6.
    system_metric_list = resource.Body("system_metric_list", type=dict)
    #: start_time
    start_time = resource.Body("start_time", type=int)
    #: Total number of the queried training job configurations.
    config_total_count = resource.Body("config_total_count", type=int)
    #: configs parameters
    configs = resource.Body("configs", type=list)
    #: Name of a training job configuration
    config_name = resource.Body("config_name", type=str)
    #: Description of a training job configuration
    config_desc = resource.Body("config_desc", type=str)
    #: Number of workers in a training job
    worker_server_num = resource.Body("worker_server_num", type=int)
    #: Code directory of a training job
    app_url = resource.Body("app_url", type=str)
    #: Boot file of a training job
    boot_file_url = resource.Body("boot_file_url", type=str)
    #: Model ID of a training job
    model_id = resource.Body("model_id", type=int)
    #: Running parameters of a training job. It is a collection of
    #:  label-value pairs. This parameter is a container environment
    #:  variable when a job uses a custom image.
    parameter = resource.Body("parameter", type=list)
    #: ID of the resource specifications selected for a training job
    spec_id = resource.Body("spec_id", type=int)
    #: Dataset of a training job
    data_url = resource.Body("data_url", type=str)
    #: Dataset ID of a training job
    dataset_id = resource.Body("dataset_id", type=str)
    #: Dataset version ID of a training job
    dataset_version_id = resource.Body("dataset_version_id", type=str)
    #: Engine type of a training job
    engine_type = resource.Body("engine_type", type=int)

    #: ID of the engine selected for a training job
    engine_id = resource.Body("engine_id", type=int)
    #: Name of the engine selected for a training job
    engine_name = resource.Body("engine_name", type=str)
    #: Version of the engine selected for a training job
    engine_version = resource.Body("engine_version ", type=str)
    #: OBS URL of the logs of a training job. By default, this parameter
    #:  is left blank. Example value: /usr/train/
    log_url = resource.Body("log_url", type=str)
    #: Resource specifications selected for a training job
    spec_code = resource.Body("spec_code", type=str)
    #: SWR URL of a custom image used by a training job
    user_image_url = resource.Body("user_image_url", type=str)
    #: Boot command used to start the container of a custom image
    #:  of a training job
    user_command = resource.Body("user_command", type=str)
    #: GPU type of the resource specifications
    gpu_type = resource.Body("gpu_type", type=str)
    #: Local mount path of SFS Turbo (NAS). Example value: /home/work/nas
    nas_mount_path = resource.Body("nas_mount_path", type=str)
    #: Shared path of SFS Turbo (NAS). Example value: 192.168.8.150:/
    nas_share_addr = resource.Body("nas_share_addr", type=str)
    #: OBS URL of the output file of a training job.
    # By default, this parameter is left blank. Example value: /usr/train/
    train_url = resource.Body("train_url", type=str)
    #: Only NFS is supported. Example value: nfs
    nas_type = resource.Body("nas_type", type=str)
    #: Time when a training job parameter configuration is created
    created_at = resource.Body("create_time", type=str)
    #: CPU memory of the resource specifications
    cpu = resource.Body("cpu", type=int)
    #: Dataset of a training job
    dataset_name = resource.Body("dataset_name", type=str)
    #: ID of a resource pool
    pool_id = resource.Body("pool_id", type=str)
    #: Number of GPUs of the resource specifications
    gpu_num = resource.Body("gpu_num", type=int)
    #: Name of a resource pool
    pool_name = resource.Body("pool_name", type=str)
    #: Dataset of a training job
    dataset_version_name = resource.Body("dataset_version_name", type=str)
    #: Number of cores of the resource specifications
    core = resource.Body("core", type=int)

    #: Datasets of a training job
    data_source = resource.Body("data_source", type=list)
    #: Storage volume that can be used by a training job.
    volumes = resource.Body("volumes", type=list)
    config = resource.Body("config", type=dict)
