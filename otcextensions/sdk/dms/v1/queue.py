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


from otcextensions.sdk.dms import dms_service
#from otcextensions.sdk.dms.v1 import dmsresource as _base
from otcextensions.sdk.dms.v1 import _base
from otcextensions.sdk import sdk_resource
_logger= _log.setup_logging('openstack')

class Queue(_base.Resource):

    resources_key = 'queues'

    base_path = '/queues'
    service = dms_service.DmsService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True

    # Properties
    #: Queue Id
    id = resource.Body('id')
    #: Queue name
    name = resource.Body('name')
     #: Queue mode
    queue_mode = resource.Body('queue_mode')   
    #: Description for the queue
    description = resource.Body('description')
    #: Redrive policy
    redrive_policy = resource.Body('redrive_policy')
     #: Max consume count number
    #: *Type: int*
    max_consume_count = resource.Body('max_consume_count', type=int)
    #: Retentions hours
    #: *Type: int*
    retention_hours = resource.Body('retention_hours', type=int)
    #: Created time
    #: *Type: int*
    created = resource.Body('created', type=int)

""" class GroupSpec(_base.Resource):
    # Properties
    #: Name
    name = resource.Body('name')


class Group(_base.Resource):

    resources_key = 'groups'

    base_path = 'queues/%(queue_id)s/groups'
    service = dms_service.DmsService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_delete = True

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')
    #: Consume roup Id
    id = resource.Body('id')
    #: groups (mandatory)
    groups = resource.Body('groups', type=list, list_type=GroupSpec)
    #: Consume group name
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

    # This does a post and return a list of self
    @classmethod
    def create_groups(cls, session, queue_id=queue_id, **kwargs):
        uri = cls.base_path % {'queue_id': queue_id}

        headers = {}
        headers.update({'Content-type': 'application/json'})
        headers.update({'Content-Length': str(len(str(kwargs)))})

        response = session.post(uri,json=kwargs, headers=headers)

        if response is not None:
            response = response.json()
            resp = response['groups']

            ret = []
            for r in resp:
                r['queue_id'] = queue_id
                ret.append(cls.existing(**r))

            return ret


class Message(_base.Resource):

    # No response for this post method
    base_path = '/queues/%(queue_id)s/messages'

    service = dms_service.DmsService()

    # capabilities
    allow_create = True

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')

    @classmethod
    def create_messages(cls, session, queue_id=queue_id, **kwargs):
        uri = cls.base_path % {'queue_id': queue_id}

        headers = {}
        headers.update({'Content-type': 'application/json'})
        headers.update({'Content-Length': str(len(str(kwargs)))})

        response = session.post(uri,json=kwargs, headers=headers)

        return response


class MessageConsumer(_base.Resource):

    base_path = '/queues/%(queue_id)s/groups/%(consumer_group_id)s/messages'

    service = dms_service.DmsService()

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
    @classmethod
    def _assemble_query_params(cls, base_url, params):
        # pop queue_id and consumer_group_id
        params.pop('queue_id', None)
        params.pop('consumer_group_id', None)
        if len(params) == 0:
            return base_url
        base_url = base_url + '?'
        for (p, v) in params.items():
            if p == 'tags':
                for tag in v:
                    base_url = base_url + 'tag=' + tag + '&'
            else:
                base_url = base_url + p + '=' + str(v) + '&'
        return base_url[:-1]

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
        base_path = 'ack'.join(self.base_path.rsplit('messages', 1))
        uri = base_path % self._uri.attributes

        body = {
            "message": [
                {
                    "handler": self.handler,
                    "status": self.status if self.status else status
                }
            ]
        }

        headers = self._header.dirty
        headers.update({'Content-type': 'application/json'})
        headers.update({'Content-Length': str(len(str(body)))})

        response = session.post(
            uri, 
            json=body, 
            headers=headers)

        self._translate_response(response)
        return self
 """

class Quota(_base.Resource):

    base_path = '/quotas/dms'
    service = dms_service.DmsService()

    allow_list = True

    # Properties
    #: Quota resource type
    type = resource.Body('type')
    #: Quota of this resource
    #: *Type: int*
    quota = resource.Body('quota', type=int)
    #: Used of this resource
    #: *Type: int*
    used = resource.Body('used', type=int)

    @classmethod
    def list(cls, session, paginated=False, **params):

        more_data = True
        query_params = cls._query_mapping._transpose(params)
        uri = cls.base_path % params
        headers = {"Accept": "application/json",
                   "Content-type": "application/json"}

        while more_data:
            resp = session.get(
                uri,
                headers=headers,
                params=query_params)
            resp = resp.json()

            # Quota for dms are a list of resources
            resp = resp['quotas']['resources']

            if not resp:
                more_data = False

            # Keep track of how many items we've yielded. If we yielded
            # less than our limit, we don't need to do an extra request
            # to get back an empty data set, which acts as a sentinel.
            yielded = 0
            new_marker = None
            for data in resp:

                value = cls.existing(**data)
                new_marker = value.id
                yielded += 1
                yield value

            if not paginated:
                return
            if "limit" in query_params and yielded < query_params["limit"]:
                return
            query_params["limit"] = yielded
            query_params["marker"] = new_marker
