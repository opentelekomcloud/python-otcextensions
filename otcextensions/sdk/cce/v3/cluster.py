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
# import six
from openstack import resource

from otcextensions.sdk.cce.v3 import _base


class HostNetworkSpec(resource.Resource):

    # Properties
    #: ID of the high-speed network that is used to create a bare metal node.
    highway_subnet = resource.Body('highwaySubnet')
    #: Security group.
    security_group = resource.Body('SecurityGroup')
    #: ID of the subnet that is used to create a node.
    network_id = resource.Body('subnet')
    #: ID of the VPC that is used to create a node.
    router_id = resource.Body('vpc')


class ClusterSpec(resource.Resource):

    #: Authentication
    authentication = resource.Body('authentication', type=dict)
    #: Billing mode of the cluster. Currently, only pay-per-use is supported.
    billing = resource.Body('billingMode')
    #: Container network parameters.
    container_network = resource.Body('containerNetwork', type=dict)
    #: Cluster description.
    description = resource.Body('description')
    #: Extended parameters.
    extended_param = resource.Body('extendParam', type=dict)
    #: Cluster flavors.
    flavor = resource.Body('flavor')
    #: Node network parameters.
    host_network = resource.Body('hostNetwork', type=HostNetworkSpec)
    #: Service forwarding mode
    kube_proxy_mode = resource.Body('kubeProxyMode')
    #: Service CIDR block or the IP address range which the kubernetes
    #: clusterIp must fall within
    service_ip_range = resource.Body('kubernetesSvcIpRange')
    #: Cluster type.
    type = resource.Body('type')
    #: Cluster version ['v1.11.7-r2', 'v1.13.10-r0'].
    version = resource.Body('version')


class StatusSpec(_base.StatusSpec):
    # Properties
    #: Access address of the kube-apiserver in the cluster.
    endpoints = resource.Body('endpoints', type=dict)


class Cluster(_base.Resource):
    base_path = '/clusters'

    resources_key = ''
    resource_key = ''

    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Properties
    #: specification
    spec = resource.Body('spec', type=ClusterSpec)
    #: Cluster status
    status = resource.Body('status', type=StatusSpec)

    @classmethod
    def new(cls, **kwargs):
        if 'kind' not in kwargs:
            kwargs['kind'] = 'Cluster'
        if 'apiVersion' not in kwargs:
            kwargs['apiVersion'] = 'v3'
        metadata = kwargs.get('metadata', '')
        if 'name' in kwargs and not metadata:
            name = kwargs.pop('name', '')
            kwargs['metadata'] = {
                'name': name
            }
        return cls(_synchronized=False, **kwargs)
