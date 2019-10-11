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
from openstack import resource
from openstack import utils


class Resource(resource.Resource):

    query_marker_key = 'offset'

    _query_mapping = resource.QueryParameters(
        'marker', 'limit',
        marker='offset',
        limit='limit'
    )

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        # AS service pagination. Returns query for the next page
        next_link = None
        params = {}
        if total_yielded < data['total_count']:
            next_link = uri
            params['offset'] = total_yielded
            params['limit'] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params, cls)
        return next_link, query_params

    def _action(self, session, body):
        """Preform alarm actions given the message body.

        """
        # if getattr(self, 'endpoint_override', None):
        #     # If we have internal endpoint_override - use it
        #     endpoint_override = self.endpoint_override
        url = utils.urljoin(self.base_path, self.id, 'action')
        return session.post(
            url,
            # endpoint_override=endpoint_override,
            json=body)
