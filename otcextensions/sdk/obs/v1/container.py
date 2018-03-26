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
from openstack import utils


from openstack.object_store.v1 import container
from otcextensions.sdk.obs.v1 import _base

from openstack import _log

_logger = _log.setup_logging('openstack')


class Container(container.Container, _base.BaseResource):

    # #should be redefined here
    # #: The name of the container.
    name = resource.Body("name", alternate_id=True)

    resources_key = 'Buckets'

    @classmethod
    def new(cls, **kwargs):
        # Container uses name as id. Proxy._get_resource calls
        # Resource.new(id=name) but then we need to do container.name
        # It's the same thing for Container - make it be the same.
        name = kwargs.pop('id', None)
        if name:
            kwargs.setdefault('name', name)
        return Container(_synchronized=True, **kwargs)

    @classmethod
    def _normalize_obs_keys(cls, entity):
        resource = {}

        name = entity.get('Name', None)
        if name:
            resource['name'] = name

        resource['x-container-object-count'] = -1
        resource['x-container-bytes-used'] = -1

        return resource

    def _translate_response(self, response, has_body=True, error_message=None):
        """Given a KSA response, inflate this instance with its data

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        # if has_body is None:
        #     has_body = self.has_body
        if response:
            if has_body:
                resource = self._normalize_obs_keys(response)
                self._update(**resource)

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

        body = self._body.dirty
        if prepend_key and self.resource_key is not None:
            body = {self.resource_key: body}

        if self.name:
            body['Bucket'] = self.name

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
        return super(Container, cls)._list(
            session, 'list_buckets', '_normalize_obs_keys',
            paginated, **params
        )

    def create(self, session, prepend_key=True):
        return super(Container, self)._create(
            session, 'create_bucket', prepend_key
        )

    def delete(self, session, error_message=None):
        return super(Container, self).delete(
            session, 'delete_bucket', error_message
        )

    def get(self, session, error_message=None, requires_id=True):
        return super(Container, self).get(
            session, 'head_bucket', error_message, requires_id
        )
