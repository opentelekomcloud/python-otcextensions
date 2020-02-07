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

    query_marker_key = 'start_number'

    _query_mapping = resource.QueryParameters(
        'marker', 'limit',
        marker='start_number',
        limit='limit'
    )

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        # AS service pagination. Returns query for the next page
        next_link = None
        params = {}
        if total_yielded < data['total_number']:
            next_link = uri
            params['marker'] = total_yielded
            params['limit'] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params, cls)
        return next_link, query_params

    @staticmethod
    def find_value_by_accessor(input_dict, accessor):
        """Gets value from a dictionary using a dotted accessor"""
        current_data = input_dict
        for chunk in accessor.split('.'):
            if isinstance(current_data, dict):
                current_data = current_data.get(chunk, {})
            else:
                return None
        return current_data

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
