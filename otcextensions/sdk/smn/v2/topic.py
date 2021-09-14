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


class Topic(resource.Resource):
    resources_key = 'topics'
    base_path = '/notifications/topics'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'offset', 'limit')

    #: Resource identifier of a topic, which is unique
    id = resource.Body('topic_urn', alternate_id=True)
    #: Time when the topic was created
    #: The UTC time is in YYYY-MM-DDTHH:MM:SSZ format.
    create_time = resource.Body('create_time')
    #: Topic display name, which is presented as the name of
    #: the email sender in email messages
    #: Contains only digits, letters, underscores and hyphens
    display_name = resource.Body('display_name')
    #: Specifies the Topic Name.
    #: Contains only digits, letters, underscores and hyphens
    name = resource.Body('name')
    #: Message push policy
    #: 0: Failed messages will be saved in message queues.
    #: 1: Failed messages will be discarded.
    push_policy = resource.Body('push_policy', type=int)
    #: Unique Request ID
    request_id = resource.Body('request_id')
    #: Time when the topic was updated
    #: The UTC time is in YYYY-MM-DDTHH:MM:SSZ format.
    update_time = resource.Body('update_time')


class AttributeSpec(resource.Resource):
    #: Properties
    #: topic access policy
    access_policy = resource.Body('access_policy')
    #: Introduction
    introduction = resource.Body('introduction')


class TopicAttribute(resource.Resource):
    base_path = '/notifications/topics/%(topic_urn)s/attributes'

    allow_list = True
    allow_commit = True
    allow_delete = True

    _query_mapping = resource.QueryParameters(
        'offset', 'limit', 'name')

    #: Properties
    #: Topic URN
    topic_urn = resource.URI('topic_urn')
    #: Unique Request ID
    request_id = resource.Body('request_id')
    #: Unique Request ID
    attributes = resource.Body('attributes', type=AttributeSpec)
    #: Values of topic attributes
    value = resource.Body('value')
