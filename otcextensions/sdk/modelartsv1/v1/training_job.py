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
from openstack import utils


class ParameterSpec(resource.Resource):
    #: Parameter name.
    label = resource.Body("label")
    #: Parameter value.
    value = resource.Body("value")
    #: Whethere parameter is required.
    required = resource.Body("required", type=bool)
    #: Placeholder.
    placeholder = resource.Body("placeholder")
    #: Tip.
    tip = resource.Body("tip", type=dict)


class HostPathSpec(resource.Resource):
    #: Local path of a training job.
    dest_path = resource.Body("dest_path")
    #: Whether dest_path is read-only.
    read_only = resource.Body("read_only", type=bool)
    #: Local path of a host.
    src_path = resource.Body("src_path")


class NfsSpec(resource.Resource):
    #: Local path of a training job.
    dest_path = resource.Body("dest_path")
    #: ID of an SFS Turbo file system.
    id = resource.Body("id")
    #: Whether dest_path is read-only.
    read_only = resource.Body("read_only", type=bool)
    #: Address of an SFS Turbo file system.
    src_path = resource.Body("src_path")


class VolumeSpec(resource.Resource):
    #: Storage volume of the host file system type.
    host_path = resource.Body("host_path", type=HostPathSpec)
    #: Storage volume of the shared file system type.
    nfs = resource.Body("nfs", type=NfsSpec)


class DataSourceSpec(resource.Resource):
    #: OBS bucket path.
    data_url = resource.Body("data_url")
    #: Dataset ID of a training job.
    dataset_id = resource.Body("dataset_id")
    #: Dataset version ID of a training job.
    dataset_version = resource.Body("dataset_version")
    #: Dataset type.
    type = resource.Body("type")


class SystemMetricListSpec(resource.Resource):
    #: CPU usage of a training job.
    cpu_usage = resource.Body("cpuUsage", type=list)
    #: GPU usage of a training job.
    gpu_util = resource.Body("gpuUtil", type=list)
    #: Memory usage of a training job.
    mem_usage = resource.Body("memUsage", type=list)
    #: Disk read rate of a training job.
    disk_read_rate = resource.Body("diskReadRate", type=list)
    #: Disk read rate of a training job.
    disk_write_rate = resource.Body("diskWriteRate", type=list)
    #: Received bytes rate of a training job.
    recv_bytes_rate = resource.Body("recvBytesRate", type=list)
    #: Send bytes rate of a training job.
    send_bytes_rate = resource.Body("sendBytesRate", type=list)
    #: GPU memory usage of a training job.
    gpu_mem_usage = resource.Body("gpuMemUsage", type=list)
    #: Interval
    interval = resource.Body("interval", type=int)


class ConfigSpec(resource.Resource):
    # Properties
    #: BuiltIn Algorithm Id.
    algorithm_id = resource.Body("algorithm_id")
    #: Training job additional Attributes.
    attributes = resource.Body("attributes", type=dict)
    #: Code directory of a training job, for example, /usr/app/.
    app_url = resource.Body("app_url")
    #: Billing resources.
    billing = resource.Body("billing", type=dict)
    #: Boot file of a training job, which needs to be stored
    #:  in the code directory.
    boot_file_url = resource.Body("boot_file_url")
    #: Number of cores of the resource specifications.
    core = resource.Body("core")
    #: CPU memory of the resource specifications.
    cpu = resource.Body("cpu")
    #: Timestamp when a training job is created.
    created_at = resource.Body("create_time", type=int)
    #: Whether a version is created when a training job is created.
    #:  Default value.
    create_version = resource.Body("create_version", type=bool)
    #: Dataset of a training job.
    data_source = resource.Body(
        "data_source", type=list, list_type=DataSourceSpec
    )
    #: OBS URL of the dataset required by a training job.
    data_url = resource.Body("data_url")
    #: Dataset ID of a training job.
    dataset_id = resource.Body("dataset_id")
    #: Dataset of a training job.
    dataset_name = resource.Body("dataset_name")
    #: Dataset version ID of a training job.
    dataset_version_id = resource.Body("dataset_version_id")
    #: Dataset of a training job.
    dataset_version_name = resource.Body("dataset_version_name")
    #: Description of a training job.
    description = resource.Body("description")
    #: Training job running duration, in milliseconds.
    duration = resource.Body("duration", type=int)
    #: ID of the engine selected for a training job.
    engine_id = resource.Body("engine_id", type=int)
    #: Name of the engine selected for a training job.
    engine_name = resource.Body("engine_name")
    #: Engine type of a training job.
    engine_type = resource.Body("engine_type", type=int)
    #: Version of the engine selected for a training job.
    engine_version = resource.Body("engine_version")
    #: Error code of a failed API call.
    error_code = resource.Body("error_code")
    #: Error message of a failed API call.
    error_message = resource.Body("error_message")
    #: Resource specification selected for a training job.
    flavor_code = resource.Body("flavor_code")
    #: Resource specifications details.
    flavor_info = resource.Body("flavor_info", type=dict)
    #: Resource specification type selected for a training job type.
    flavor_type = resource.Body("flavor_type")
    #: GPU memory unit.
    gpu_memory_unit = resource.Body("gpu_memory_unit")
    #: Number of GPUs of the resource specifications.
    gpu_num = resource.Body("gpu_num", type=int)
    #: GPU type of the resource specifications.
    gpu_type = resource.Body("gpu_type")
    #: Whether the resource specification used for training is free.
    is_free = resource.Body("is_free")
    #: Whether the request is successful.
    is_success = resource.Body("is_success", type=bool)
    #: Whether training job is in Zombie to state.
    is_zombie = resource.Body("is_zombie", type=bool)
    #: Description of a training job.
    job_desc = resource.Body("job_desc")
    #: ID of a training job.
    job_id = resource.Body("job_id", type=int, alternate_id=True)
    #: Name of a training job.
    job_name = resource.Body("job_name")
    #: Training job type.
    job_type = resource.Body("job_type", type=int)
    #: OBS URL of the logs of a training job.
    log_url = resource.Body("log_url")
    #: Max count.
    max_num = resource.Body("max_num", type=int)
    #: Memory unit.
    memory_unit = resource.Body("memory_unit")
    #: Model metrics of a training job.
    model_metric_list = resource.Body("model_metric_list")
    #: ID of the built-in model of a training job.
    model_id = resource.Body("model_id", type=int)
    #: Name of a training job.
    name = resource.Body("name", alias="job_name")
    #: Local mount path of SFS Turbo (NAS).
    nas_mount_path = resource.Body("nas_mount_path")
    #: Shared path of SFS Turbo (NAS).
    nas_share_addr = resource.Body("nas_share_addr")
    #: Only NFS is supported.
    nas_type = resource.Body("nas_type")
    #: Whether no resource.
    no_resource = resource.Body("no_resource", type=bool)
    #: NPU Info.
    npu_info = resource.Body("npu_info")
    #: Running parameters of a training job.
    parameter = resource.Body("parameter", type=list, list_type=ParameterSpec)
    #: Pod Version.
    pod_version = resource.Body("pod_version")
    #: ID of a resource pool.
    pool_id = resource.Body("pool_id")
    #: Name of a resource pool.
    pool_name = resource.Body("pool_name")
    #: Resource pool type.
    pool_type = resource.Body("pool_type")
    #: Name of the previous version of a training job.
    pre_version_id = resource.Body("pre_version_id", type=int)
    #: Charged resource ID of a training job.
    resource_id = resource.Body("resource_id")
    #: Model Id used for re-training.
    retrain_model_id = resource.Body("retrain_model_id")
    #: Resource specifications selected for a training job.
    spec_code = resource.Body("spec_code")
    #: ID of the resource specifications selected for a training job.
    spec_id = resource.Body("spec_id", type=int)
    #: Training start time.
    started_at = resource.Body("start_time", type=int)
    #: Status of a training job.
    status = resource.Body("status", type=int)
    #: System monitoring metrics of a training job.
    system_metric_list = resource.Body(
        "system_metric_list", type=SystemMetricListSpec
    )
    #: OBS URL of the output file of a training job.
    train_url = resource.Body("train_url")
    #: Boot command used to start the container of a
    #:  custom image of a training job.
    user_command = resource.Body("user_command")
    #: SWR URL of a custom image used by a training job.
    user_image_url = resource.Body("user_image_url")
    #: Number of versions of a training job.
    version_count = resource.Body("version_count", type=int)
    #: Version ID of a training job.
    version_id = resource.Body("version_id", type=int)
    #: Version name of a training job.
    version_name = resource.Body("version_name")
    #: Storage volume that can be used by a training job.
    volumes = resource.Body("volumes", type=list, list_type=VolumeSpec)
    #: Number of workers in a training job.
    worker_server_num = resource.Body("worker_server_num", type=int)


class TrainingJob(ConfigSpec):
    base_path = "/training-jobs"

    resources_key = "jobs"

    # capabilities
    allow_commit = True
    allow_create = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        "limit",
        "order",
        "offset",
        "search_content",
        "sort_by",
        "status",
        "workspace_id",
        limit="per_page",
        offset="page",
        sort_by="sortBy",
    )

    #: Parameters for creating a training job.
    config = resource.Body("config", type=ConfigSpec)
    #: Description of a training job.
    job_desc = resource.Body("job_desc")
    #: Training job name.
    job_name = resource.Body("job_name")
    #: Workspace where a job resides.
    workspace_id = resource.Body("workspace_id")

    def stop(self, session, version_id):
        """Preform actions given the message body."""
        uri = utils.urljoin(
            "training-jobs", self.id, "versions", version_id, "stop"
        )
        response = session.post(uri, json=None)
        self._translate_response(response)
        return self
