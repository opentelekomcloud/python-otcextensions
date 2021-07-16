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
# from openstack import exceptions
from openstack import resource
from openstack.dns.v2 import recordset

from urllib import parse


class Recordset(recordset.Recordset):
    """DNS Recordset Resource"""

    _query_mapping = resource.QueryParameters(
        'name', 'type', 'ttl', 'data', 'status', 'description',
        'limit', 'marker', 'offset', 'tags')

    #: Properties
    #: Is the recordset created by system.
    is_default = resource.Body('default', type=bool)
    #: Timestamp when the zone was last updated.
    updated_at = resource.Body('update_at')

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        next_link = None
        params = {}
        if isinstance(data, dict):
            links = data.get('links')
            if links:
                next_link = links.get('next')
            total = data.get('metadata', {}).get('total_count')
            if total:
                # We have a kill switch
                total_count = int(total)
                if total_count <= total_yielded:
                    return None, params

        # Parse params from Link (next page URL) into params.
        # This prevents duplication of query parameters that with large
        # number of pages result in HTTP 414 error eventually.
        if next_link:
            parts = parse.urlparse(next_link)
            query_params = parse.parse_qs(parts.query)
            params.update(query_params)
            next_link = parse.urljoin(next_link,
                                      parts.path)

        # If we still have no link, and limit was given and is non-zero,
        # and the number of records yielded equals the limit, then the user
        # is playing pagination ball so we should go ahead and try once more.
        if not next_link:
            next_link = uri
            params['marker'] = marker
            if limit:
                params['limit'] = limit
        return next_link, params
