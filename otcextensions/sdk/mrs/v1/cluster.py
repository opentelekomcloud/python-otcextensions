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

from openstack import _log
from openstack import resource

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class ClusterInfo(sdk_resource.Resource):
    resource_key = 'cluster'
    resources_key = 'clusters'
    base_path = '/cluster_infos'

    # capabilities
    allow_list = True
    allow_get = True

    _query_mapping = resource.QueryParameters(
        'status', 'marker', 'limit',
        'project_id', 'tags',
        status='clusterState',
        marker='currentPage',
        limit='pageSize')

    cluster_id = resource.URI('cluster_id')

    #: Properties
    #: Cluster ID.
    id = resource.Body('clusterId', alternate_id=True)
    #: Cluster name.
    name = resource.Body('clusterName')
    #: Number of Master nodes deployed in a cluster.
    master_num = resource.Body('masterNodeNum')
    #: Number of Core nodes deployed in a cluster.
    core_num = resource.Body('coreNodeNum')
    #: Total number of nodes deployed in a cluster.
    total_num = resource.Body('totalNodeNum')
    #: Cluster status.
    status = resource.Body('clusterState')
    #: Cluster creation time, which is a 10-bit timestamp.
    created_at = resource.Body('createAt')
    #: Cluster update time, which is a 10-bit timestamp.
    updated_at = resource.Body('updateAt')
    #: Cluster billing mode
    billing_type = resource.Body('billingType')
    #: Cluster work region.
    region = resource.Body('dataCenter')
    #: VPC name.
    vpc = resource.Body('vpc')
    #: Cluster creation fee, which is automatically calculated.
    fee = resource.Body('fee')
    #: Hadoop version.
    hadoop_version = resource.Body('hadoopVersion')
    #: Instance specifications of a Master node.
    master_node_size = resource.Body('masterNodeSize')
    #: Instance specifications of a Core node.
    core_node_size = resource.Body('coreNodeSize')
    #: Component list.
    component_list = resource.Body('componentList', type=list)
    #: External IP address.
    external_ip = resource.Body('externalIp')
    #: Backup external IP address.
    external_alternate_ip = resource.Body('externalAlternateIp')
    #: Internal IP address.
    internal_ip = resource.Body('internalIp')
    #: Cluster deployment ID
    deployment_id = resource.Body('deploymentId')
    #: Cluster remarks.
    remark = resource.Body('remark')
    #: Cluster creation order ID.
    order_id = resource.Body('orderId')
    #: AZ name.
    az = resource.Body('azName')
    #: AZ ID.
    az_id = resource.Body('azId')
    #: Product ID of a Master node.
    master_node_product_id = resource.Body('masterNodeProductId')
    #: Specification ID of a Master node.
    master_node_spec_id = resource.Body('masterNodeSpecId')
    #: Product ID of a Core node.
    core_node_product_id = resource.Body('coreNodeProductId')
    #: Specification ID of a Core node.
    core_node_spec_id = resource.Body('coreNodeSpecId')
    #: Instance ID.
    instance_id = resource.Body('instanceId')
    #: URI for remotely logging in to an ECS.
    vnc = resource.Body('vnc')
    #: Project ID.
    project_id = resource.Body('tenantId')
    #: Disk storage space.
    volume_size = resource.Body('volumeSize', type=int)
    #: Disk type.
    volume_type = resource.Body('volumeType')
    #: Subnet ID.
    subnet_id = resource.Body('subnetId')
    #: Subnet name.
    subnet_name = resource.Body('subnetName')
    #: Cluster type.
    cluster_type = resource.Body('clusterType')
    #: Security group ID.
    security_group_id = resource.Body('securityGroupsId')
    #: Security group ID of a non-Master node.
    non_master_security_group_id = resource.Body('slaveSecurityGroupsId')
    #: Cluster operation progress description.
    stage_desc = resource.Body('stageDesc')
    #: Whether MRS Manager installation is finished during cluster creation.
    mrs_install_state = resource.Body('mrsManagerFinish', type=bool)
    #: Running mode of an MRS cluster.
    safe_mode = resource.Body('safeMode')
    #: Cluster version.
    cluster_version = resource.Body('clusterVersion')
    #: Name of the key file.
    key = resource.Body('nodePublicCertName')
    #: IP address of a Master node.
    master_ip = resource.Body('masterNodeIp')
    #: Preferred private IP address.
    preffered_private_ip = resource.Body('privateIpFirst')
    #: Error message.
    error_info = resource.Body('errorInfo')
    #: Start time of billing.
    charging_start_time = resource.Body('chargingStartTime')
    #: Whether to collect logs when cluster installation fails.
    log_collection = resource.Body('logCollection', type=int)
    #: List of Task nodes.
    task_node_groups = resource.Body('taskNodeGroups', type=list)
    #: List of Master, Core and Task nodes.
    node_groups = resource.Body('nodeGroups', type=list)
    #: Data disk storage type of the Master node.
    #: SATA, SAS and SSD are supported.
    master_data_volume_type = resource.Body('masterDataVolumeType')
    #: Data disk storage space of the Master node.
    master_data_volume_size = resource.Body('masterDataVolumeSize', type=int)
    #: Number of data disks of the Master node.
    master_data_volume_count = resource.Body('masterDataVolumeCount', type=int)
    #: Data disk storage type of the Core node.
    core_data_volume_type = resource.Body('coreDataVolumeType')
    #: Data disk storage space of the Core node.
    core_data_volume_size = resource.Body('coreDataVolumeSize', type=int)
    #: Data disk storage space of the Core node.
    core_data_volume_count = resource.Body('coreDataVolumeCount', type=int)
    #: Bootstrap action script information.
    bootstrap_scripts = resource.Body('bootstrap_scripts', type=list)
    #: Bootstrap action script information.
    tags = resource.Body('tags', type=list)
    #: Node change status.
    scale = resource.Body('scale')


class Host(sdk_resource.Resource):
    resources_key = 'hosts'
    base_path = '/clusters/%(cluster_id)s/hosts'

    # capabilities
    allow_list = True
    allow_get = True

    _query_mapping = resource.QueryParameters(
        'marker', 'limit',
        marker='currentPage',
        limit='pageSize')

    cluster_id = resource.URI('cluster_id')

    #: Properties
    #: VM ID
    id = resource.Body('id', alternate_id=True)
    #: VM IP address
    ip = resource.Body('ip')
    #: VM flavor ID
    flavor = resource.Body('flavor')
    #: VM type
    type = resource.Body('type')
    #: VM name
    name = resource.Body('name')
    #: Current VM state
    status = resource.Body('status')
    #: Memory
    mem = resource.Body('mem')
    #: Number of CPU cores
    cpu = resource.Body('cpu')
    #: OS disk capacity
    root_volume_size = resource.Body('root_volume_size')
    #: Data disk type
    data_volume_type = resource.Body('data_volume_type')
    #: Data disk capacity
    data_volume_size = resource.Body('data_volume_size')
    #: Number of data disks
    data_volume_count = resource.Body('data_volume_count')
