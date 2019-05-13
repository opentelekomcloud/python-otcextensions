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
    def list(cls, session, paginated=True, base_path=None, **params):
        """This method is a generator which yields resource objects.

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param bool paginated: ``True`` if a GET to this resource returns
                               a paginated series of responses, or ``False``
                               if a GET returns only one page of data.
                               **When paginated is False only one
                               page of data will be returned regardless
                               of the API's support of pagination.**
        :param str base_path: Base part of the URI for listing resources, if
                              different from
                              :data:`~openstack.resource.Resource.base_path`.
        :param dict params: These keyword arguments are passed through the
            :meth:`~openstack.resource.QueryParamter._transpose` method
            to find if any of them match expected query parameters to be
            sent in the *params* argument to
            :meth:`~keystoneauth1.adapter.Adapter.get`. They are additionally
            checked against the
            :data:`~openstack.resource.Resource.base_path` format string
            to see if any path fragments need to be filled in by the contents
            of this argument.

        :return: A generator of :class:`Resource` objects.
        :raises: :exc:`~openstack.exceptions.MethodNotSupported` if
                 :data:`Resource.allow_list` is not set to ``True``.
        :raises: :exc:`~openstack.exceptions.InvalidResourceQuery` if query
                 contains invalid params.
        """
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")
        session = cls._get_session(session)
        microversion = cls._get_microversion_for_list(session)

        if base_path is None:
            base_path = cls.base_path
        cls._query_mapping._validate(params, base_path=base_path)
        query_params = cls._query_mapping._transpose(params)
        uri = base_path % params

        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'},
                params=query_params.copy())
            exceptions.raise_from_response(response)

            if response.json() and 'items' in response.json():
                data = response.json()['items'] or []

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            for raw_resource in resources:

                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    **raw_resource)
                yield value

            return
