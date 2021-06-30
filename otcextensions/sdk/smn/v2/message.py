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


class Message(resource.Resource):
    base_path = '/notifications/topics/{topic_urn}s/publish'

    # capabilities
    allow_create = True

    #: Message ID, which is unique
    message_id = resource.Body('message_id')
    #: Request ID, which is unique.
    request_id = resource.Body('request_id')
    #: Message subject, which is used as the email
    #: subject when you publish email messages.
    subject = resource.Body('subject')
    #: Message content.
    #: The message content is a UTF-8-coded character string of
    #: no more than 256 KB. For SMS subscribers, if the content
    #: exceeds 256 bytes, the system will divide it into multiple
    #: messages and send only the first two.
    message = resource.Body('message')
    #: Message structure, which contains JSON character strings.
    #: Specify protocols in the structure, which can be http,
    #: https, email, dms, and sms.
    message_structure = resource.Body('message_structure')
    #: Message template name, which can be obtained according
    #: to Querying Message Templates
    message_template_name = resource.Body('message_template_name')
    #: Time-to-live (TTL) of a message, specifically, the maximum time
    #: period for retaining the message in the system
    time_to_live = resource.Body('time_to_live')
