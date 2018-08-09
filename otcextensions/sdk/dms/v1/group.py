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
# from openstack import utils

from otcextensions.sdk.dms.v1 import _base

_logger = _log.setup_logging('openstack')


class Group(_base.Resource):

    # NOTE: we are not interested in the also returned short queue info
    resources_key = 'groups'

    base_path = 'queues/%(queue_id)s/groups'
    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'include_deadletter'
    )

    # Properties
    queue_id = resource.URI('queue_id')

    #: Consume group Id
    id = resource.Body('id')
    #: Name
    name = resource.Body('name')
    #: Total message number, not including deleted message
    #: *Type: int*
    produced_messages = resource.Body('produced_messages', type=int)
    #: Consumed message number
    #: *Type: int*
    consumed_messages = resource.Body('consumed_messages', type=int)
    #: Available message number
    #: *Type: int*
    available_messages = resource.Body('available_messages', type=int)
    #: Total deadletters number
    #: *Type: int*
    produced_deadletters = resource.Body('produced_deadletters', type=int)
    #: Available deadletters number
    #: *Type: int*
    available_deadletters = resource.Body('available_deadletters', type=int)

    def create(self, session, group):
        """create group"""
        body = {"groups": [{'name': group}]}

        request = self._prepare_request(requires_id=False,
                                        prepend_key=False)

        response = session.post(
            request.url,
            json=body,
            headers={'Content-Length': str(len(str(body)))})

        # Squize groups into single response entity
        resp = response.json()
        if self.resources_key in resp:
            res = resp[self.resources_key][0]

            res = self._consume_body_attrs(res)
            self._body.attributes.update(res)
            self._body.clean()

        return self
