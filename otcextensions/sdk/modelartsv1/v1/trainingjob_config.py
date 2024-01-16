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


class Param(resource.Resource):
    pass


class DataSource(resource.Resource):
    #: Dataset ID of a training job
    dataset_id = resource.Body("dataset_id", type=str)
    #: Dataset version ID of a training job
    dataset_version = resource.Body("dataset_version", type=str)
    #: Dataset type. Possible values are as follows: obs: Data from
    #:  OBS is used. dataset: Data from a specified dataset is used.
    type = resource.Body("data_type", type=int)
    #: OBS bucket path
    data_url = resource.Body("data_path", type=str)


class NFS(resource.Resource):
    #: ID of an SFS Turbo file system
    id = resource.Body("id", type=str)
    #: Address of an SFS Turbo file system
    src_path = resource.Body("src_path", type=str)
    #: Local path of a training job
    dest_path = resource.Body("dest_path", type=str)
    #: Whether dest_path is read-only. The default value is false.
    #: \n`true`: read-only permission
    #: \n`false`: read/write permission.
    read_only = resource.Body("read_only", type=bool)


class HostPath(resource.Resource):
    pass


class Volume(resource.Resource):
    #: Storage volume of the shared file system type. Only
    #:  the training jobs running in the resource pool with the
    #:  shared file system network connected support such storage volume.
    nfs = resource.Body("nfs ", type=NFS)
    #: Storage volume of the host file system type. Only training jobs
    #:  running in the dedicated resource pool support such storage volume.
    host_path = resource.Body("host_path", type=HostPath)


class HostPath(resource.Resource):
    #: Local path of a host
    src_path = resource.Body("src_path", type=str)
    #: Local path of a training job
    dest_path = resource.Body("dest_path", type=str)
    #: Whether dest_path is read-only. The default value is false.
    #: \ntrue: read-only permission
    #: \nfalse: read/write permission. This is the default value.
    read_only = resource.Body("read_only", type=bool)


class Config(resource.Resource):
    #: Name of a training job configuration
    config_name = resource.Body("config_name", type=str)
    #: Description of a training job configuration
    config_desc = resource.Body("config_desc", type=str)
    #: Time when a training job is created
    create_time = resource.Body("create_time", type=float)
    #: Engine type of a training job
    engine_type = resource.Body("engine_type", type=int)
    #: Name of the engine selected for a training job
    engine_name = resource.Body("engine_name", type=str)
    #: ID of the engine selected for a training job
    engine_id = resource.Body("engine_id", type=float)
    #: Version of the engine selected for a training job
    engine_version = resource.Body("engine_version", type=str)
    #: SWR URL of a custom image used by a training job.
    #:  Example value: 100.125.5.235:20202/jobmng/custom-cpu-base:1.0
    user_image_url = resource.Body("user_image_url", type=str)
    #: Boot command used to start the container of a
    #:  custom image of a training job.
    user_command = resource.Body("user_command", type=str)


class TrainingjobConfig(resource.Resource):
    base_path = "/training-job-configs"

    resources_key = ""
    resource_key = ""

    allow_create = True
    allow_list = True
    allow_commit = True
    allow_delete = True
    allow_fetch = True
    allow_patch = True

    #: Whether the request is successful
    is_success = resource.Body("is_success", type=bool)
    #: Error message of a failed API call. This parameter
    #:  is not included when the API call succeeds.
    error_msg = resource.Body("error_msg", type=bool)
    #: Error code of a failed API call. For details, see Error Code.
    # This parameter is not included when the API call succeeds.
    error_code = resource.Body("error_code", type=bool)

    #: Total number of the queried training job configurations
    config_total_count = resource.Body("config_total_count", type=int)
    #: configs parameters
    configs = resource.Body("configs", type=list, list_type=Config)
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
    model_id = resource.Body("model_id", type=float)
    #: Running parameters of a training job. It is a collection
    #:  of label-value pairs. This parameter is a container
    #:  environment variable when a job uses a custom image.
    parameter = resource.Body("parameter", type=list, list_type=Param)
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
    #: OBS URL of the logs of a training job. By default,
    #:  this parameter is left blank. Example value: /usr/train/
    log_url = resource.Body("log_url", type=str)
    #: Resource specifications selected for a training job
    spec_code = resource.Body("spec_code", type=str)
    #: SWR URL of a custom image used by a training job
    user_image_url = resource.Body("user_image_url", type=str)
    #: Boot command used to start the container of a
    #:  custom image of a training job
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
    create_time = resource.Body("create_time", type=float)
    #: CPU memory of the resource specifications
    cpu = resource.Body("cpu", type=str)
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
    core = resource.Body("core", type=str)

    #: Datasets of a training job
    data_source = resource.Body("data_source", type=list, list_type=DataSource)
    #: Storage volume that can be used by a training job.
    volumes = resource.Body("volumes", type=Volume)
