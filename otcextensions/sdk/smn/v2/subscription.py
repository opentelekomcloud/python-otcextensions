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
    base_path = '/notifications/topics/%(topic_urn)s/subscriptions'

    # capabilities
    allow_create = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'offset', 'limit')

    #: Resource identifier of a subscription, which is unique
    id = resource.Body('subscription_urn', alternate_id=True)
    #: Message receiving endpoint
    endpoint = resource.Body('endpoint')
    #: Subscription protocol
    #: Following protocols are supported:
    #: email, sms, http and https
    protocol = resource.Body('protocol')
    #: Project ID of the topic creator
    owner = resource.Body('owner')
    #: Remarks
    remark = resource.Body('remark')
    #: Subscription status
    #:  0: unconfirmed
    #:  1: confirmed
    #:  3: canceled
    status = resource.Body('status')
    #: Resource identifier of a topic, which is unique
    topic_urn = resource.URI('topic_urn')

    def delete(self, session, error_message=None, **kwargs):
        self.base_path = '/notifications/subscriptions'
        return super(Subscription, self).delete(
            session,
            error_message=error_message,
            **kwargs)

    @classmethod
    def list(cls, session, paginated=True, base_path=None,
             allow_unknown_params=False, **params):
        if not params.get('topic_urn'):
            base_path = '/notifications/subscriptions'
        return super(Subscription, cls).list(
            session=session,
            paginated=paginated,
            base_path=base_path,
            allow_unknown_params=allow_unknown_params,
            **params)
