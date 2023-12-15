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
from urllib import parse

from openstack import proxy


class Proxy(proxy.Proxy):

    skip_discovery = True

    def _extract_name(self, url, service_type=None, project_id=None):
        path = parse.urlparse(url).path.strip()
        # Remove / from the beginning to keep the list indexes of interesting
        # things consistent
        if path.startswith('/'):
            path = path[1:]

        # Split url into parts and exclude potential project_id in some urls
        url_parts = [
            x for x in path.split('/') if (
                    x != project_id
                    and (
                            not project_id
                            or (project_id and x != project_id)
                    ))
        ]
        # exclude version
        url_parts = list(filter(lambda x: not any(c.isdigit() for c in x[1:]) and (x[0].lower() != 'v'), url_parts))

        # Strip out anything that's empty or None
        return [part for part in url_parts if part]
