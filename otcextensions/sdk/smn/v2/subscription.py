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


class Subscription(resource.Resource):
    resources_key = 'subscriptions'
    base_path = '/notifications/subscriptions'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'offset', 'limit')

    #: Unique Request ID
    request_id = resource.Body('request_id')
    #: Specifies the Topic Name.
    #: Contains only digits, letters, underscores and hyphens
    name = resource.Body('name')
    #: Topic display name, which is presented as the name
    #:  of the email sender in email messages
    #: Contains only digits, letters, underscores and hyphens
    display_name = resource.Body('display_name')
    #: Resource identifier of a topic, which is unique
    topic_urn = resource.Body('topic_urn')
    #: Subscription protocol
    #: Following protocols are supported:
    #:  email, sms, http and https
    protocol = resource.Body('protocol')
    #: Resource identifier of a subscription, which is unique
    subscription_urn = resource.Body('subscription_urn')
    #: Project ID of the topic creator
    owner = resource.Body('owner')
    #: Message receiving endpoint
    endpoint = resource.Body('endpoint')
    #: Remarks
    remark = resource.Body('remark')
    #: Subscription status
    #:  0: unconfirmed
    #:  1: confirmed
    status = resource.Body('status')
