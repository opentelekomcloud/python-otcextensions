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


class Resource(resource.Resource):

    resources_key = 'tags'
    resource_key = 'tag'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'key'
    )

    # Properties
    #: Specifies listener
    listener_id = resource.URI('listener_id')
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

        body = self._prepare_request_body(patch, prepend_key)
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
