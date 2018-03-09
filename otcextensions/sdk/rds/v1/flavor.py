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
    # id = resource.Body('id', alias='str_id')
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
    id = resource.Body('str_id', alternate_id=True)
    #: Flavor detail
    #: *Type:list*
    flavor_detail = resource.Body('flavor_detail', type=list, list_type=dict)
    #: Flavor
    #: *Type:dict*
    flavor = resource.Body('flavor', type=dict)
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
            # if self.resource_key and self.resource_key in body:
            #     body = body[self.resource_key]

            body = self._consume_body_attrs(body)
            self._body.attributes.update(body)

            # Because of the response type (inline structure)
            # we need to reconsume (overwrite some) attributes
            if self.resource_key and self.resource_key in body:
                body = body[self.resource_key]

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
        # Try to short-circuit by looking directly for a matching ID.
        try:
            match = cls.existing(
                id=name_or_id,
                **params)
            return match.get(
                session,
                endpoint_override=endpoint_override,
                headers=headers)
        except (exceptions.NotFoundException, exceptions.HttpException):
            pass

        data = cls.list(session,
                        endpoint_override=endpoint_override,
                        headers=headers,
                        **params)

        result = cls._get_one_match(name_or_id, data)
        # Update result with URL parameters
        result._update(**params)
        if result is not None:
            # Refetch flavor to get details
            result = result.get(session,
                                endpoint_override=endpoint_override,
                                headers=headers)
            return result

        if ignore_missing:
            return None
        raise exceptions.ResourceNotFound(
            "No %s found for %s" % (cls.__name__, name_or_id))
