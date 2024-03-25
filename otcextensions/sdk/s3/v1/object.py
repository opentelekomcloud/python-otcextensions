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

from otcextensions.sdk.obs.v1 import _base


_logger = _log.setup_logging('openstack')


class Object(_base.BaseResource):

    resources_key = 'Object'
    resource_key = 'Objects'

    allow_get = True
    allow_head = True
    allow_list = True
    allow_create = True
    allow_delete = True

    create_method = 'PUT'

    base_path = '/'

    # all requests (except create) will default to requires_id = None
    requires_id = None

    last_modified = None
    content_type = None
    etag = None
    accept_ranges = None
    content_length = None
    key = None
    storage_class = None
    size = None

    def _translate_response(self, response, has_body=None, error_message=None):

        body_attrs = {}
        if response.get("Grants"):
            body_attrs['grants'] = response.get("Grants")

        response = response.get('ResponseMetadata')
        location = response.get('Location', None)
        if response.get('HTTPHeaders', None):
            self._header.attributes.update(response.get('HTTPHeaders'))
            if response.get('HTTPHeaders').get('location'):
                location = response.get('HTTPHeaders').get('location')
        body_attrs['location'] = location
        if location:
            body_attrs['name'] = location.split("/")[1]
        self._body.clean()
        self._body.attributes.update(body_attrs)
        dict.update(self, self.to_dict())
        return self

    def _translate_container_response(self, container):
        body_attrs = {}
        body_attrs['name'] = container.get('Name', None)
        body_attrs['creation_date'] = container.get('CreationDate', None)
        self._body.attributes.update(body_attrs)
        dict.update(self, self.to_dict())
        return self
