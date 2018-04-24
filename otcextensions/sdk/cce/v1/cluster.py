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
from openstack import utils

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.cce import cce_service
from otcextensions.sdk.cce.v1 import _base
from otcextensions.sdk.cce.v1 import cluster_host


class HostListSpec(sdk_resource.Resource):
    # Properties
    host_list = resource.Body('hostList', type=list,
                              list_type=cluster_host.ClusterHost)


class ClusterHostList(_base.Resource):
    # Properties
    #: Spec
    spec = resource.Body('spec', type=HostListSpec)


class ClusterSpec(sdk_resource.Resource):

    # Properties
    #: Description
    #: *Type:str
    description = resource.Body('description')
    #: Availability zone
    #: *Type:str*
    availability_zone = resource.Body('az')
    #: CPU size
    #: *Type:int*
    cpu = resource.Body('cpu', type=int)
    #: Memory size
    #: *Type:int*
    memory = resource.Body('memory', type=int)
    #: VPC
    #: *Type:str*
    vpc = resource.Body('vpc')
    #: VPC_ID
    #: *Type:str*
    vpc_id = resource.Body('vpcid')
    #: Subnet name
    #: *Type:str*
    subnet = resource.Body('subnet')
    #: CIDR
    #: *Type:str*
    cidr = resource.Body('cidr')
    #: Cluster type
    #: *Type:str*
    cluster_type = resource.Body('clustertype')
    #: Security group id
    #: *Type:str*
    security_group_id = resource.Body('security_group_id')
    #: Endpoint
    #: *Type:str*
    endpoint = resource.Body('endpoint')
    #: External endpoint
    #: *Type:str*
    external_endpoint = resource.Body('external_endpoint')
    #: Cluster type
    #: *Type:str*
    type = resource.Body('clustertype')
    #: host list
    host_list = resource.Body('hostList', type=ClusterHostList)
    #: Region (used for create cluster)
    region = resource.Body('region')
    #: Public IP ID or EIP ID (used for create cluster)
    publicip_id = resource.Body('publicip_id')


class Cluster(_base.Resource):
    base_path = '/clusters'

    service = cce_service.CceService()

    resources_key = ''
    resource_key = ''

    allow_list = True
    allow_get = True
    allow_create = True
    allow_update = True
    allow_delete = True

    # Properties
    #: specification
    spec = resource.Body('spec', type=ClusterSpec)
    #: Cluster status
    status = resource.Body('clusterStatus', type=dict)

    # @staticmethod
    # def _get_id(value):
    #     """If a value is a Resource, return the canonical ID
    #
    #     This will return either the value specified by `id` or
    #     `alternate_id` in that order if `value` is a Resource.
    #     If `value` is anything other than a Resource, likely to
    #     be a string already representing an ID, it is returned.
    #     """
    #     print('in the _get_id')
    #     if isinstance(value, resource.Resource):
    #         return value.metadata.id
    #     else:
    #         return value

    def __getattribute__(self, name):
        """Return an attribute on this instance

        This is mostly a pass-through except for a specialization on
        the 'id' name, as this can exist under a different name via the
        `alternate_id` argument to resource.Body.
        """
        if name == 'id' or name == 'name':
            if name in self._body:
                return self._body[name]
            else:
                try:
                    metadata = self._body['metadata']
                    if name == 'id':
                        if isinstance(metadata, dict):
                            return metadata['uuid']
                        elif isinstance(metadata, _base.Metadata):
                            return metadata._body[metadata._alternate_id()]
                    else:
                        if isinstance(metadata, dict):
                            return metadata['name']
                        elif isinstance(metadata, _base.Metadata):
                            return metadata.name
                except KeyError:
                    return None
        else:
            return object.__getattribute__(self, name)

    def delete_nodes(self, session, node_names, headers=None):
        """Delete nodes from the cluster by their name
        """
        nodes = []
        if isinstance(node_names, list):
            # Is given a list
            for node in node_names:
                nodes.append({'name': node})
        elif isinstance(node_names, str):
            # a single string, consider as a name of single host
            nodes.append({'name': node_names})
        message = {
            'hosts': nodes
        }

        # Build additional arguments to the DELETE call
        args = self._prepare_override_args(
            additional_headers=headers
        )

        url = utils.urljoin(self.base_path, self.id, 'hosts')
        session.delete(url, json=message, **args)

    # @classmethod
    # def flatten(cls, **kwargs):
    #     result_dict = {}
    #     for (k, v) in six.iteritems(kwargs):
    #         if isinstance(v, dict):
    #             for (new_k, new_v) in six.iteritems(cls.flatten(**v)):
    #                 key = k + '.' + new_k
    #                 result_dict[key] = new_v
    #         else:
    #             result_dict[k] = v
    #     return result_dict
