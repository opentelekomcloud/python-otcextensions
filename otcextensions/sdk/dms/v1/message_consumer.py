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
from openstack import _log

from otcextensions.sdk.dms.v1 import _base
_logger = _log.setup_logging('openstack')


class MessageConsumer(_base.Resource):

    base_path = '/queues/%(queue_id)s/groups/%(consumer_group_id)s/messages'

    _query_mapping = resource.QueryParameters('max_msgs', 'time_wait')

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')
    #: Consumer group id
    consumer_group_id = resource.URI('consumer_group_id')
    #: Message dict
    #: *Type: dict
    message = resource.Body('message', type=dict)
    #: handler
    handler = resource.Body('handler')
    #: Status of the message
    status = resource.Body('status')
    #: Success number of the message
    #: *Type: int
    success = resource.Body('success', type=int)
    #: Fail number of the message
    #: *Type: int
    fail = resource.Body('fail', type=int)

    # NOTES: this API is so different from others, it's not a RESTFUL
    # style, allow user to pass mulitple tags as the query parameters
    # which can not leverage method of session directlly.
    # return an url with query params
    # it accepts multiple query params e.g. tag=tag1&tag=tag2
    # @classmethod
    # def _assemble_query_params(cls, base_url, params):
    #     # pop queue_id and consumer_group_id
    #     params.pop('queue_id', None)
    #     params.pop('consumer_group_id', None)
    #     if len(params) == 0:
    #         return base_url
    #     base_url = base_url + '?'
    #     for (p, v) in params.items():
    #         if p == 'tags':
    #             for tag in v:
    #                 base_url = base_url + 'tag=' + tag + '&'
    #         else:
    #             base_url = base_url + p + '=' + str(v) + '&'
    #     return base_url[:-1]

    # use get method to consume message, return a list of self
    @classmethod
    def list(cls, session, paginated=False, **params):

        headers = {"Accept": "application/json",
                   "Content-type": "application/json"}
        uri = cls.base_path % params

        # NOTES: this API is so different from others, it's not a RESTFUL
        # style, allow user to pass mulitple tags as the query parameters
        # which can not leverage method of session directlly.

        query_params = cls._query_mapping._transpose(params)
        resp = session.get(
            uri,
            headers=headers,
            params=query_params)

        if resp is not None:
            resp = resp.json()
            ret = []
            # resp is a list
            for r in resp:
                r['queue_id'] = params.get('queue_id')
                r['consumer_group_id'] = params.get('consumer_group_id')
                ret.append(cls.existing(**r))

            return ret

    def ack(self, session, status='success'):
        base_path = '/queues/%(queue_id)s/groups/%(consumer_group_id)s/ack'

        uri = base_path % self._uri.attributes

        body = {
            "message": [
                {
                    "handler": self.handler,
                    "status": self.status if self.status else status
                }
            ]
        }

        response = session.post
        (
            uri,json=body
        )

        self._translate_response(response)
        return self
