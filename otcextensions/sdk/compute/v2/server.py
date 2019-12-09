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
from openstack import utils

from openstack.compute.v2 import server


class Server(server.Server):

    def _get_tag_struct(self, tag):
        tag_pairs = tag.split('=')
        if len(tag_pairs) == 2:
            (k, v) = (tag_pairs[0], tag_pairs[1])
        else:
            (k, v) = (tag, "")
        return {
            'key': k,
            'value': v
        }

    def add_tag(self, session, tag):
        """Adds a single tag to the resource.

        :param session: The session to use for making this request.
        :param tag: The tag as a string.
        """
        session = self._connection.ecs
        url = utils.urljoin('servers', self.id,
                            'tags', 'action')
        body = {
            'action': 'create',
            'tags': [self._get_tag_struct(tag)]
        }
        response = session.post(url, json=body)
        exceptions.raise_from_response(response)
        # we do not want to update tags directly
        tags = self.tags
        tags.append(tag)
        self._body.attributes.update({
            'tags': list(set(tags))
        })
        return self

    def remove_tag(self, session, tag):
        """Removes a single tag from the specified server.

        :param session: The session to use for making this request.
        :param tag: The tag as a string.
        """
        session = self._connection.ecs
        url = utils.urljoin('servers', self.id,
                            'tags', 'action')
        body = {
            'action': 'delete',
            'tags': [self._get_tag_struct(tag)]
        }
        response = session.post(url, json=body)
        exceptions.raise_from_response(response)
        # we do not want to update tags directly
        tags = self.tags
        try:
            # NOTE(gtema): if tags were not fetched, but request suceeded
            # it is ok. Just ensure tag does not exist locally
            tags.remove(tag)
        except ValueError:
            pass  # do nothing!
        self._body.attributes.update({
            'tags': tags
        })
        return self
