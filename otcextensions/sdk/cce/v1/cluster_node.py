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
from openstack import exceptions
from openstack import resource

from otcextensions.sdk import sdk_resource
from otcextensions.sdk.cce.v1 import _base


class VolumeSpec(sdk_resource.Resource):
    # Properties
    #: Disk Type (root, data)
    disk_type = resource.Body('diskType')
    #: Disk Size (40G for root, 100G-32768G for data)
    disk_size = resource.Body('diskSize', type=int)
    #: Volume type (SATA, SAS, SSD)
    volume_type = resource.Body('volumeType')


class CapacitySpec(sdk_resource.Resource):
    # Properties
    #: CPU
    #: *Type: str*
    cpu = resource.Body('cpu')
    #: Memory
    #: *Type: str*
    memory = resource.Body('memory')
    #: Pods
    #: *Type: str*
    pods = resource.Body('pods')


class StatusSpec(sdk_resource.Resource):
    # Properties
    #: Capacity - maximal resources capacity
    #: *Type: CapacitySpec*
    capacity = resource.Body('capacity', type=CapacitySpec)
    #: Allocatable - available resources capacity
    #: *Type: CapacitySpec*
    allocatable = resource.Body('allocatable', type=CapacitySpec)
    #: Conditions - health conditions
    conditions = resource.Body('conditions', type=list, list_type=dict)


class NodeSpec(sdk_resource.Resource):
    # Properties
    #: Cluster UUID
    cluster_uuid = resource.Body('clusteruuid')
    #: Private IP
    private_ip = resource.Body('privateip')
    #: Public IP
    public_ip = resource.Body('publicip')
    #: Flavor (mandatory)
    flavor = resource.Body('flavor')
    #: Label
    label = resource.Body('label')
    #: CPU
    cpu = resource.Body('cpu')
    #: Memory
    memory = resource.Body('memory')
    #: availability zone
    availability_zone = resource.Body('az')
    #: volume (mandatory)
    volume = resource.Body('volume', type=list, list_type=VolumeSpec)
    #: SSH Key (mandatory)
    ssh_key = resource.Body('sshkey')
    #: status
    status = resource.Body('status', type=StatusSpec)
    #: Tags (array in format key.value)
    tags = resource.Body('tags', type=list)
    #: assign_floating_ip - whether to assign floating IP to the server
    #: (used only during create)
    #: *Type:bool*
    assign_floating_ip = resource.Body('snat', type=bool)
    #: tags (only used in creation). Format: "KEY.VALUE"
    #: *Type:list*
    tags = resource.Body('tags', type=list)


class ClusterNode(_base.Resource):
    base_path = '/clusters/%(cluster_uuid)s/hosts'
    allow_create = True
    allow_delete = True
    allow_list = True
    allow_get = True
    # Responses do not have body
    # has_body = False

    # Properties
    #: Spec
    spec = resource.Body('spec', type=NodeSpec)
    #: Status
    status = resource.Body('status')
    #: Replicas count
    replica_count = resource.Body('replicas', type=int)
    #: Message
    message = resource.Body('message')

    cluster_uuid = resource.URI('cluster_uuid')

    @classmethod
    def new(cls, **kwargs):
        if 'kind' not in kwargs:
            kwargs['kind'] = 'host'
        if 'apiVersion' not in kwargs:
            kwargs['apiVersion'] = 'v1'
        return cls(_synchronized=False, **kwargs)

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

    @classmethod
    def list(cls, session,
             endpoint_override=None, headers=None, **params):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        session = cls._get_session(session)

        # cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = cls.base_path % params

        # Build additional arguments to the GET call
        get_args = cls._prepare_override_args(
            endpoint_override=endpoint_override,
            additional_headers=headers)

        while uri:
            response = session.get(
                uri,
                params=query_params.copy(),
                **get_args
            )
            exceptions.raise_from_response(response)
            data = response.json()
            spec = data.get('spec', None)
            resources = []
            if spec:
                resources = spec.get('hostList', [])

            for raw_resource in resources:
                # Do not allow keys called "self" through. Glance chose
                # to name a key "self", so we need to pop it out because
                # we can't send it through cls.existing and into the
                # Resource initializer. "self" is already the first
                # argument and is practically a reserved word.
                raw_resource.pop("self", None)

                if cls.resource_key and cls.resource_key in raw_resource:
                    raw_resource = raw_resource[cls.resource_key]

                value = cls.existing(**raw_resource)

                yield value
            return

    def delete(self, session, error_message=None,
               endpoint_override=None, headers=None, params=None):
        """Delete the remote resource based on this instance.

        This function overrides default Resource.delete to enable headers

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`

        :return: This :class:`Resource` instance.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_update` is not set to ``True``.
        """
        if not self.allow_delete:
            raise exceptions.MethodNotSupported(self, "delete")

        request = self._prepare_request(requires_id=False)
        session = self._get_session(session)

        # Build additional arguments to the DELETE call
        delete_args = self._prepare_override_args(
            endpoint_override=endpoint_override,
            request_headers=request.headers,
            additional_headers=headers)
        if params:
            delete_args['params'] = params

        body = {
            'hosts': [
                {'name': self.name}
            ]
        }

        response = session.delete(request.url,
                                  json=body,
                                  **delete_args)
        kwargs = {}
        if error_message:
            kwargs['error_message'] = error_message

        self._translate_response(response, has_body=False, **kwargs)
        return self

    def create(self, session, prepend_key=True, requires_id=True,
               endpoint_override=None, headers=None):
        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, "create")

        session = self._get_session(session)

        if self.create_method == 'PUT':
            request = self._prepare_request(requires_id=True,
                                            prepend_key=prepend_key)
            req_args = self._prepare_override_args(
                endpoint_override=endpoint_override,
                request_headers=request.headers,
                additional_headers=headers)
            response = session.put(request.url,
                                   json=request.body, **req_args)
        elif self.create_method == 'POST':
            request = self._prepare_request(requires_id=False,
                                            prepend_key=prepend_key)
            req_args = self._prepare_override_args(
                endpoint_override=endpoint_override,
                request_headers=request.headers,
                additional_headers=headers)
            response = session.post(request.url,
                                    json=request.body, **req_args)
        else:
            raise exceptions.ResourceFailure(
                msg="Invalid create method: %s" % self.create_method)

        # This is an only difference to the existing sdk_resource.create
        self._translate_response(response, has_body=False)

        return self
