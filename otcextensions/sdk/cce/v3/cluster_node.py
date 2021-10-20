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


class VolumeSpec(resource.Resource):
    # Properties
    #: Disk Size in GB.
    size = resource.Body('size', type=int)
    #: Volume type: [SATA, SAS, SSD].
    type = resource.Body('volumetype')


class StatusSpec(_base.StatusSpec):
    # Properties
    #: ID of the VM where the node resides in the ECS.
    instance_id = resource.Body('serverId')
    #: Elastic IP address of a node.
    floating_ip = resource.Body('publicIP')
    #: Private IP address of a node.
    private_ip = resource.Body('privateIP')


class PublicIPSpec(resource.Resource):
    # Properties:
    #: List of IDs for the existing floating ips.
    ids = resource.Body('ids', type=list)
    #: Count of the IP addresses to be dynamically created.
    count = resource.Body('count', type=int)
    #: Elastic IP address. Dict of {
    #:     type,
    #:     bandwidth:{
    #:        chargemode, size, sharetype
    #:     }
    #: }.
    floating_ip = resource.Body('eip', type=dict)


class TagSpec(resource.Resource):
    # Properties:
    #: Key of the tag
    key = resource.Body('key')
    #: Value of the tag
    value = resource.Body('value')


class TaintSpec(resource.Resource):
    # Properties:
    #: A key can contain letters, digits, hyphens, underscores and periods
    #: up to 63 characters starting with letter or digit.
    key = resource.Body('key')
    #: A value can contain letters, digits, hyphens, underscores and periods
    #: up to 63 characters starting with letter or digit.
    value = resource.Body('value')
    #: Effect available options: NoSchedule, PreferNoSchedule, NoExecute
    effect = resource.Body('effect')


class ExtendParamSpec(resource.Resource):
    # Properties:
    #: Script required before the installation
    #: Input must be Base64 encoded
    preinstall_script = resource.Body('alpha.cce/preInstall')
    #: Script required after the installation
    #: Input must be Base64 encoded
    postinstall_script = resource.Body('alpha.cce/postInstall')
    #: ConfigMap of the Docker data disk
    lvm_config = resource.Body('DockerLVMConfigOverride')
    #: Maximum number of pods on the node
    max_pods = resource.Body('maxPods', type=int)
    #: ID of a custom node image
    #: Mandatory if custom image is used on a bare metall node
    node_image_id = resource.Body('alpha.cce/NodeImageID')


class NodeSpec(resource.Resource):
    # Properties
    #: Name of the AZ where the node resides.
    availability_zone = resource.Body('az')
    #: Billing mode of a node. Currently, only pay-per-use is supported.
    billing_mode = resource.Body('billingMode', type=int, default=0)
    #: Number of nodes.
    count = resource.Body('count', type=int)
    #: Data disk parameters of a node. At present, only one data
    #: disk can be configured
    data_volumes = resource.Body('dataVolumes', type=list,
                                 list_type=VolumeSpec)
    #: ID of the Dedicated Host to which nodes will be scheduled
    dedicated_host = resource.Body('dedicatedHostId')
    #: ID of the ECS group where the CCE node can belong to
    ecs_group = resource.Body('ecsGroupId')
    # Extended parameters in key-value format
    extend_params = resource.Body('extendParam', type=ExtendParamSpec)
    #: The node is created in the specified fault domain.
    fault_domain = resource.Body('faultDomain')
    #: Flavor (mandatory)
    flavor = resource.Body('flavor')
    #: Elastic IP address parameters of a node.
    floating_ip = resource.Body('publicIP', type=PublicIPSpec)
    #: Kubernetes tags
    k8s_tags = resource.Body('k8sTags', type=dict)
    #: Parameters for logging in to the node.
    login = resource.Body('login')
    #: Boolean: if node is offloading all its components
    offload_node = resource.Body('offloadNode', type=bool)
    #: Operating System of the node. EulerOS and CentOS are supported.
    os = resource.Body('os')
    #: System disk parameters of the node.
    root_volume = resource.Body('rootVolume', type=VolumeSpec)
    #: Tags of a Node
    tags = resource.Body('userTags', type=list, list_type=TagSpec)
    #: Taints are used to configure anti-affinity
    taints = resource.Body('taints', type=list, list_type=TaintSpec)


class ClusterNode(_base.Resource):

    base_path = '/clusters/%(cluster_id)s/nodes'

    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Properties
    #: Cluster id.
    cluster_id = resource.URI('cluster_id')
    #: Spec
    spec = resource.Body('spec', type=NodeSpec)
    #: Status
    status = resource.Body('status', type=StatusSpec)

    @classmethod
    def new(cls, **kwargs):
        if 'kind' not in kwargs:
            kwargs['kind'] = 'Node'
        if 'apiVersion' not in kwargs:
            kwargs['apiVersion'] = 'v3'
        return cls(_synchronized=False, **kwargs)
