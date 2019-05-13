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

from otcextensions.sdk.cce.v3 import _base


class VolumeSpec(resource.Resource):
    # Properties
    #: Disk Size in GB.
    size = resource.Body('size', type=int)
    #: Volume type: [SATA, SAS, SSD].
    type = resource.Body('volumetype')


class StatusSpec(resource.Resource):
    # Properties
    #: ID of the VM where the node resides in the ECS.
    instance_id = resource.Body('serverId')
    #: Elastic IP address of a node.
    floating_ip = resource.Body('publicIP')
    #: Private IP address of a node.
    private_ip = resource.Body('privateIP')
    #: Status.
    status = resource.Body('phase')


class PublicIPSpec(resource.Resource):
    # Properties:
    #: List of IDs for the existing floating ips.
    ids = resource.Body('ids')
    #: Count of the IP addresses to be dynamically created.
    count = resource.Body('count', type=int)
    #: Elastic IP address. Dict of {
    #:     type,
    #:     bandwidth:{
    #:        chargemode, size, sharetype
    #:     }
    #: }.
    floating_ip = resource.Body('eip', type=dict)


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
    #: Flavor (mandatory)
    flavor = resource.Body('flavor')
    #: Elastic IP address parameters of a node.
    floating_ip = resource.Body('publicIP', type=PublicIPSpec)
    #: Parameters for logging in to the node.
    login = resource.Body('login')
    #: Operating System of the node. Currently only EulerOS is supported.
    os = resource.Body('os')
    #: System disk parameters of the node.
    root_volume = resource.Body('rootVolume', type=VolumeSpec)
    #: Node status.
    status = resource.Body('status', type=StatusSpec)


class ClusterNode(_base.Resource):

    base_path = '/clusters/%(cluster_id)s/nodes'

    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Properties
    cluster_id = resource.URI('cluster_id')
    #: Spec
    spec = resource.Body('spec', type=NodeSpec)
    #: Status
    status = resource.Body('status')

    @classmethod
    def new(cls, **kwargs):
        if 'kind' not in kwargs:
            kwargs['kind'] = 'node'
        if 'apiVersion' not in kwargs:
            kwargs['apiVersion'] = 'v3'
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
                            return metadata['uid']
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
        query_params = cls._query_mapping._transpose(params)
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
