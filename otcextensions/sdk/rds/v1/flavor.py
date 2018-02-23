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
    id = resource.Body('id')
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
    str_id = resource.Body('str_id')
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
