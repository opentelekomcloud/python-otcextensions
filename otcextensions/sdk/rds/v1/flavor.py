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

from openstack import exceptions

from otcextensions.sdk.rds import rds_service

from otcextensions.sdk import sdk_resource

_logger = _log.setup_logging('openstack')


class Flavor(sdk_resource.Resource):

    base_path = '/%(project_id)s/flavors'
    # In difference to regular OS services RDS
    # does not return single item with a proper element tag
    resource_key = 'flavor'
    resources_key = 'flavors'
    service = rds_service.RdsService()

    # capabilities
    allow_get = True
    allow_list = True

    project_id = resource.URI('project_id')
    # Properties
    #: Flavor id
    id = None
    #: Flavor name
    name = resource.Body('name')
    #: Ram size in MB.
    #: *Type:int*
    ram = resource.Body('ram', type=int)
    #: Instance created time
    specCode = resource.Body('specCode')
    #: Links
    #: *Type:list*
    # links = resource.Body('links', type=list)
    #: String id
    str_id = resource.Body('str_id', alternate_id=True)
    #: Flavor detail
    #: *Type:list*
    flavor_detail = resource.Body('flavor_detail', type=list, list_type=dict)
    #: Flavor
    #: *Type:dict*
    # flavor = resource.Body('flavor', type=dict)
    #: Price detail
    #: *Type:list*
    price_detail = resource.Body('price_detail', type=list)

    links = resource.Body('links', type=list)

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response, error_message=error_message)
        if has_body:
            body = response.json()
            # throw away id
            body.pop('id', None)

            # Because of the response type (inline structure)
            # we need to reconsume (overwrite some) attributes
            if self.resource_key and self.resource_key in body:
                body['ram'] = body[self.resource_key]['ram']

            body = self._consume_body_attrs(body)
            self._body.attributes.update(body)

            self._body.clean()

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()

    @classmethod
    def find(cls, session, name_or_id, ignore_missing=True,
             endpoint_override=None, headers=None, **params):
        """Find a resource by its name or id.

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param name_or_id: This resource's identifier, if needed by
                           the request. The default is ``None``.
        :param bool ignore_missing: When set to ``False``
                    :class:`~openstack.exceptions.ResourceNotFound` will be
                    raised when the resource does not exist.
                    When set to ``True``, None will be returned when
                    attempting to find a nonexistent resource.
        :param dict params: Any additional parameters to be passed into
                            underlying methods, such as to
                            :meth:`~openstack.resource.Resource.existing`
                            in order to pass on URI parameters.

        :return: The :class:`Resource` object matching the given name or id
                 or None if nothing matches.
        :raises: :class:`openstack.exceptions.DuplicateResource` if more
                 than one resource is found for this request.
        :raises: :class:`openstack.exceptions.ResourceNotFound` if nothing
                 is found and ignore_missing is ``False``.
        """
        # invoke class method to find entity
        result = super(Flavor, cls).find(
            # Flavor,
            # cls,
            session,
            name_or_id,
            ignore_missing=ignore_missing,
            endpoint_override=endpoint_override,
            headers=headers,
            **params
        )

        if result and not result.flavor_detail:
            # Unfortuantely flavor_detail is missing due to list not having
            # all the details. Refetch the entity directly
            result = result.get(
                session,
                endpoint_override=endpoint_override,
                headers=headers)
            return result
        else:
            return result

    @classmethod
    def existing(cls, **kwargs):
        """Create an instance of an existing remote resource.

        When creating the instance set the ``_synchronized`` parameter
        of :class:`Resource` to ``True`` to indicate that it represents the
        state of an existing server-side resource. As such, all attributes
        passed in ``**kwargs`` are considered "clean", such that an immediate
        :meth:`update` call would not generate a body of attributes to be
        modified on the server.

        :param dict kwargs: Each of the named arguments will be set as
                            attributes on the resulting Resource object.
        """
        # eject corrupted id for py2
        if 'str_id' in kwargs:
            kwargs.pop('id', None)
        return cls(_synchronized=True, **kwargs)
