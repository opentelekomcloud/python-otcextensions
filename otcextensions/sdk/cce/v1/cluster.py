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
import six

# from openstack import exceptions
from openstack import resource

from otcextensions.sdk import sdk_resource

from otcextensions.sdk.cce import cce_service


class Metadata(sdk_resource.Resource):

    # Properties
    #: UUID
    #: *Type:str
    id = resource.Body('uuid', alternate_id=True)
    #: Name
    #: *Type:str
    name = resource.Body('name')
    #: Space UUID
    #: *Type:str
    space_uuid = resource.Body('spaceuuid')
    #: Create time
    #: *Type:str
    create_time = resource.Body('createAt')
    #: Update time
    #: *Type:str
    update_time = resource.Body('updateAt')


class Spec(sdk_resource.Resource):

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


class Cluster(sdk_resource.Resource):
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
    #: Kind
    kind = resource.Body('kind')
    #: metadata
    metadata = resource.Body('metadata', type=Metadata)
    #: specification
    spec = resource.Body('spec', type=Spec)
    #: host list
    host_list = resource.Body('hostList', type=list)

    @staticmethod
    def _get_id(value):
        """If a value is a Resource, return the canonical ID

        This will return either the value specified by `id` or
        `alternate_id` in that order if `value` is a Resource.
        If `value` is anything other than a Resource, likely to
        be a string already representing an ID, it is returned.
        """
        print('in the _get_id')
        if isinstance(value, resource.Resource):
            return value.metadata.id
        else:
            return value

    def __getattribute__(self, name):
        """Return an attribute on this instance

        This is mostly a pass-through except for a specialization on
        the 'id' name, as this can exist under a different name via the
        `alternate_id` argument to resource.Body.
        """
        if name == "id":
            if name in self._body:
                return self._body[name]
            else:
                try:
                    metadata = self._body['metadata']
                    if isinstance(metadata, dict):
                        return metadata['uuid']
                    elif isinstance(metadata, Metadata):
                        return metadata._body[metadata._alternate_id()]
                except KeyError:
                    return None
        else:
            return object.__getattribute__(self, name)

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
