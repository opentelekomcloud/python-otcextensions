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
from openstack import (resource, exceptions)
from openstack import utils

from otcextensions.sdk.elb.v2 import _base


class Tag(_base.Resource):
    resources_key = 'tags'
    base_path = ('/loadbalancers/%(loadbalancer_id)s/tags')

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    # Properties
    #: Specifies load balancer
    loadbalancer_id = resource.URI('loadbalancer_id')
    #: Specifies the tag key
    key = resource.Body('key')
    #: Specifies the tag value
    value = resource.Body('value')

    def _prepare_request(self, requires_id=None, prepend_key=False,
                         patch=False, base_path=None, params=None, **kwargs):
        """Prepare a request to be sent to the server

        Create operations don't require an ID, but all others do,
        so only try to append an ID when it's needed with
        requires_id. Create and update operations sometimes require
        their bodies to be contained within an dict -- if the
        instance contains a resource_key and prepend_key=True,
        the body will be wrapped in a dict with that key.
        If patch=True, a JSON patch is prepared instead of the full body.

        Return a _Request object that contains the constructed URI
        as well a body and headers that are ready to send.
        Only dirty body and header contents will be returned.
        """
        if requires_id is None:
            requires_id = self.requires_id

        body = {
            'tag': self._prepare_request_body(patch, prepend_key)
        }
        headers = {}

        if base_path is None:
            base_path = self.base_path
        uri = base_path % self._uri.attributes
        if requires_id:
            if self.id is None:
                raise exceptions.InvalidRequest(
                    "Request requires an ID but none was found")

            uri = utils.urljoin(uri, self.id)

        uri = utils.urljoin(self.location.project['id'], uri)

        return resource._Request(uri, body, headers)

    @classmethod
    def list(cls, session, base_path=None,
             allow_unknown_params=True, **params):
        """This method is a generator which yields resource objects.

        This resource object list generator handles pagination and takes query
        params for response filtering.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str base_path: Base part of the URI for listing resources, if
            different from :data:`~openstack.resource.Resource.base_path`.
        :param bool allow_unknown_params: ``True`` to accept, but discard
            unknown query parameters. This allows getting list of 'filters' and
            passing everything known to the server. ``False`` will result in
            validation exception when unknown query parameters are passed.
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
        if base_path is None:
            base_path = cls.base_path
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=allow_unknown_params)
        uri = base_path % params

        while uri:
            response = session.get(
                session.get_project_id() + uri,
                headers={"Accept": "application/json"},
            )
            exceptions.raise_from_response(response)
            data = response.json()

            if cls.resources_key:
                resources = data[cls.resources_key]
            else:
                resources = data

            if not isinstance(resources, list):
                resources = [resources]

            for raw_resource in resources:
                value = cls.existing(
                    connection=session._get_connection(),
                    **raw_resource)
                yield value

            return
