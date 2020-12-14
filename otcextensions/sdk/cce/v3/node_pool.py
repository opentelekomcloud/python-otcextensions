#!/usr/bin/env python3
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

from otcextensions.sdk.cce.v3 import _base


class VolumeExtendParams(resource.Resource):
    # Properties
    # Usage mode of data disk e.g. docker
    use_type = resource.Body('useType')


class DataVolumeEncryptionSpec(resource.Resource):
    # Properties
    # Whether an EVS disk is encrypted (1) or not (0).
    encrypted = resource.Body('__system__encrypted', type=bool, default=False)
    # CMK ID used for encryption.
    cmk_id = resource.Body('__system__cmkid')


class VolumeSpec(resource.Resource):
    # Properties
    # Disk Size in GB.
    size = resource.Body('size', type=int)
    # Volume type: [SATA, SAS, SSD].
    type = resource.Body('volumetype')


class DataVolumeSpec(VolumeSpec):
    # Properties
    # Extended fields in dictionary format
    extend_params = resource.Body('extendParam', type=VolumeExtendParams)
    # Mandatory data if data encryption of the data Volume is necessary.
    # If data disks are created using a data disk image, this parameter
    # cannot be used.
    metadata = resource.Body('metadata', type=DataVolumeEncryptionSpec)


class PublicIPSpec(resource.Resource):
    # Properties:
    # List of IDs for the existing floating ips.
    ids = resource.Body('ids')
    # Count of the IP addresses to be dynamically created.
    count = resource.Body('count', type=int)
    # Elastic IP address. Dict of {
    #     type,
    #     bandwidth:{
    #        chargemode, size, sharetype
    #     }
    # }.
    floating_ip = resource.Body('eip', type=dict)


class TagSpec(resource.Resource):
    # Properties:
    # Key of the tag
    key = resource.Body('key')
    # Value of the tag
    value = resource.Body('value')


class TaintSpec(resource.Resource):
    # Properties:
    # A key can contain letters, digits, hyphens, underscores and periods
    # up to 63 characters starting with letter or digit.
    key = resource.Body('key')
    # A value can contain letters, digits, hyphens, underscores and periods
    # up to 63 characters starting with letter or digit.
    value = resource.Body('value')
    # Effect available options: NoSchedule, PreferNoSchedule, NoExecute
    effect = resource.Body('effect')


class ExtendParamSpec(resource.Resource):
    # Properties:
    # Script required before the installation
    # Input must be Base64 encoded
    preinstall_script = resource.Body('alpha.cce/preInstall')
    # Script required after the installation
    # Input must be Base64 encoded
    postinstall_script = resource.Body('alpha.cce/postInstall')
    # ConfigMap of the Docker data disk
    lvm_config = resource.Body('DockerLVMConfigOverride')
    # Maximum number of pods on the node
    max_pods = resource.Body('maxPods', type=int)
    # ID of a custom node image
    # Mandatory if custom image is used on a bare metall node
    node_image_id = resource.Body('alpha.cce/NodeImageID')
    # Public key of the node.
    public_key = resource.Body('publicKey')


class AutoScalingSpec(resource.Resource):
    # Enable or disable auto scaling
    enable = resource.Body('enable', type=bool)
    # Minimum number of nodes after a scale-up if auto-scaling is enabled.
    min_node_count = resource.Body('minNodeCount', type=int)
    # Maximum number of nodes after scale-up, if auto-scaling is enabled.
    # The value must be equal or greater than min_node_count and cannot
    # exceed the maximum number of nodes of the cluster.
    max_node_count = resource.Body('maxNodeCount', type=int)
    # Node pool weight. A higher weight indicates a higher priority
    # in scale-up.
    priority = resource.Body('priority', type=int)
    # Interval in minutes during which nodes added aafter a scale-up
    # will not be deleted.
    scale_down_cooldown_time = resource.Body('scaleDownCooldownTime', type=int)


class NodeManagementSpec(resource.Resource):
    # ECS groupt id of the ECS group to which those nodes belong
    # after creation.
    ecs_group_id = resource.Body('serverGroupReference')


class SubnetIdSpec(resource.Resource):
    # ID of the subnet to which the NIC belongs
    subnet_id = resource.Body('subnetId')


class NodeNicSpec(resource.Resource):
    # Description about the primary NIC
    primary_nic = resource.Body('primaryNic', type=SubnetIdSpec)


class NodeTemplateSpec(resource.Resource):
    # Properties
    # Name of the AZ where the node resides.
    # If availability_zone is set to: random, nodes can be created in any AZ
    availability_zone = resource.Body('az')
    # Billing mode of a node. Currently, only pay-per-use is supported.
    billing_mode = resource.Body('billingMode', type=int, default=0)
    # Number of nodes.
    count = resource.Body('count', type=int)
    # Data disk parameters of a node. At present, only one data
    # disk can be configured
    data_volumes = resource.Body('dataVolumes', type=list,
                                 list_type=DataVolumeSpec)
    # ID of the Dedicated Host to which nodes will be scheduled
    dedicated_host = resource.Body('dedicatedHostId')
    # ID of the ECS group where the CCE node can belong to
    ecs_group = resource.Body('ecsGroupId')
    # Extended parameters in key-value format
    extend_params = resource.Body('extendParam', type=ExtendParamSpec)
    # The node is created in the specified fault domain.
    fault_domain = resource.Body('faultDomain')
    # Flavor (mandatory)
    flavor = resource.Body('flavor')
    # Elastic IP address parameters of a node.
    floating_ip = resource.Body('publicIP', type=PublicIPSpec)
    # Kubernetes tags
    k8s_tags = resource.Body('k8sTags', type=dict)
    # Parameters for logging in to the node.
    login = resource.Body('login')
    node_nic_spec = resource.Body('nodeNicSpec', type=NodeNicSpec)
    # Boolean: if node is offloading all its components
    offload_node = resource.Body('offloadNode', type=bool)
    # Operating System of the node. EulerOS and CentOS (K8s version >= 1.17)
    # are supported.
    os = resource.Body('os')
    # System disk parameters of the node.
    root_volume = resource.Body('rootVolume', type=VolumeSpec)
    # Tags of a Node
    tags = resource.Body('userTags', type=list, list_type=TagSpec)
    # Taints are used to configure anti-affinity
    taints = resource.Body('taints', type=list, list_type=TaintSpec)


class NodePoolSpec(resource.Resource):
    # Autoscaling parameters
    autoscaling = resource.Body('autoscaling', type=AutoScalingSpec)
    # Expected number of nodes in this node pool.
    initial_node_count = resource.Body('initialNodeCount', type=int)
    node_management = resource.Body('nodeManagement', type=NodeManagementSpec)
    # Node pool type. Currently only ECSs are supported
    # Value: vm
    node_pool_type = resource.Body('type')
    # Template of the node specification.
    node_template_spec = resource.Body('nodeTemplate', type=NodeTemplateSpec)


class MetaDataSpec(resource.Body):
    # Name of the node pool
    name = resource.Body('name')
    #: UUID
    #: *Type:str
    id = resource.Body('uid', alternate_id=True)


class NodePool(_base.Resource):

    base_path = '/clusters/%(cluster_id)s/nodepools'

    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Properties
    # Cluster id.
    cluster_id = resource.URI('cluster_id')
    # Spec
    spec = resource.Body('spec', type=NodePoolSpec)
    # other metadata
    metadata = resource.Body('metadata', type=MetaDataSpec)

    @classmethod
    def new(cls, **kwargs):
        if 'kind' not in kwargs:
            kwargs['kind'] = 'NodePool'
        if 'apiVersion' not in kwargs:
            kwargs['apiVersion'] = 'v3'
        return cls(_synchronized=False, **kwargs)
