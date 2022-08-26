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


class Message(resource.Resource):

    resource_key = 'message'
    base_path = '/queues/%(queue_id)s/groups/%(group_id)s/messages'

    allow_list = True

    _query_mapping = resource.QueryParameters(
        'max_msgs', 'time_wait', 'ack_wait'
    )

    #: Queue id
    queue_id = resource.URI('queue_id')
    #: Group ID (part of URL for listing)
    group_id = resource.URI('group_id')

    # Properties
    #: Attributes
    attributes = resource.Body('attributes', type=dict)
    #: Message body
    body = resource.Body('body')
    #: Error info
    error = resource.Body('error')
    #: Error code
    error_code = resource.Body('error_code')
    #: Message handler (ID)
    handler = resource.Body('handler', alternate_id=True)
    #: State (0 - success)
    state = resource.Body('state', type=int)

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):

        microversion = cls._get_microversion(session, action='list')

        if base_path is None:
            base_path = cls.base_path
        params = cls._query_mapping._validate(
            params, base_path=base_path,
            allow_unknown_params=allow_unknown_params)
        query_params = cls._query_mapping._transpose(params, cls)
        uri = base_path % params

        while uri:
            # Copy query_params due to weird mock unittest interactions
            response = session.get(
                uri,
                headers={"Accept": "application/json"},
                params=query_params.copy(),
                microversion=microversion)
            exceptions.raise_from_response(response)
            data = response.json()
            resources = data

            if not isinstance(resources, list):
                resources = [resources]

            for raw_resource in resources:
                attrs = raw_resource.pop('message')
                handler = raw_resource.pop('handler')
                value = cls.existing(
                    microversion=microversion,
                    connection=session._get_connection(),
                    id=handler,
                    **attrs)
                yield value

            if not resources:
                return


class Messages(resource.Resource):

    resources_key = 'messages'
    base_path = '/queues/%(queue_id)s/messages'

    # capabilities
    allow_create = True
    allow_list = True

    # Properties
    #: Queue id
    queue_id = resource.URI('queue_id')
    #: Messages
    messages = resource.Body('messages', type=list, list_type=Message)
    #: Whether message ID should be returned
    return_id = resource.Body('returnId', type=bool)
