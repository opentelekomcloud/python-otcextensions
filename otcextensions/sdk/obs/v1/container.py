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
import xml.etree.ElementTree as ET

from openstack import _log
from openstack import exceptions
from openstack import resource
from openstack import utils

from otcextensions.sdk.obs.v1 import _base


_logger = _log.setup_logging('openstack')


class Container(_base.BaseResource):

    resources_key = 'Buckets'
    resource_key = 'Bucket'

    allow_get = True
    allow_head = True
    allow_list = True
    allow_create = True
    allow_delete = True

    create_method = 'PUT'

    base_path = '/'

    # all requests (except create) will default to requires_id = None
    requires_id = None

    name = resource.Body('Name', alternate_id=True, alias='id')
    creation_date = resource.Body('CreationDate')

    storage_class = resource.Header('x-default-storage-class')

    def _translate_response(self, response, has_body=True, error_message=None):
        """Given a KSA response, inflate this instance with its data

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        exceptions.raise_from_response(response, error_message=response.text)
        if response:
            if has_body:
                # TODO(agoncharov): do nothing so far. Generally need
                # to parse different responses
                pass

    def _prepare_request(self, requires_id=None, prepend_key=False):
        """Prepare a request to be sent to the server

        Create operations don't require an ID, but all others do,
        so only try to append an ID when it's needed with
        requires_id. Create and update operations sometimes require
        their bodies to be contained within an dict -- if the
        instance contains a resource_key and prepend_key=True,
        the body will be wrapped in a dict with that key.

        Return a _Request object that contains the constructed URI
        as well a body and headers that are ready to send.
        Only dirty body and header contents will be returned.
        """
        if requires_id is None:
            requires_id = self.requires_id

        body = None
        # body = self._body.dirty
        # if prepend_key and self.resource_key is not None:
        #     body = {self.resource_key: body}

        # if self.name:
        #     body['Bucket'] = self.name

        base_path = '/'
        headers = {}
        uri = base_path % self._uri.attributes
        if requires_id:
            if self.id is None:
                raise exceptions.InvalidRequest(
                    "Request requires an ID but none was found")

            uri = utils.urljoin(uri, self.id)

        return resource._Request(uri, body, headers)

    @classmethod
    def list(cls, session, paginated=False, **params):
        if not cls.allow_list:
            raise exceptions.MethodNotSupported(cls, "list")

        cls._query_mapping._validate(params, base_path=cls.base_path)
        query_params = cls._query_mapping._transpose(params, cls)

        response = session.get(
            session.get_endpoint(),
            params=query_params.copy(),
        )

        root = ET.fromstring(response.content)

        if root.tag != ET.QName(cls.OBS_NS, 'ListAllMyBucketsResult'):
            _logger.warn('Namespace in the response does not match '
                         'expectation')
            cls.OBS_NS = root.tag.split('}', 1)[0][1:]

        for elements in root:

            if elements.tag == ET.QName(cls.OBS_NS, cls.resources_key):
                for el in elements:
                    if el.tag == ET.QName(cls.OBS_NS, cls.resource_key):
                        # Convert XML part into dict
                        dict_raw_resource = cls.etree_to_dict(el)
                        # extract resource data
                        dict_resource = dict_raw_resource[cls.resource_key]
                        value = cls.existing(**dict_resource)
                        yield value

        return

    def create(self, session, prepend_key=True, base_path=None, **params):

        if not self.allow_create:
            raise exceptions.MethodNotSupported(self, "create")

        session = self._get_session(session)

        request = self._prepare_request()

        response = session.put(request.url,
                               data=request.body, **params)

        self._translate_response(response)
        return self
