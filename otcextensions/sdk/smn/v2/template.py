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


class Template(resource.Resource):
    resources_key = 'message_templates'
    base_path = '/notifications/message_template'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_commit = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'offset', 'limit', 'protocol', 'name',
        name='message_template_name')

    #: Unique Request ID
    id = resource.Body('id', alias='message_template_id')
    message_template_id = resource.Body('message_template_id')
    #: Specifies the Template Name.
    #: Contains only digits, letters, underscores and hyphens.
    message_template_name = resource.Body('message_template_name')
    #: Protocol supported by the template.
    protocol = resource.Body('protocol')
    #: Template content, which currently supports plain text only.
    content = resource.Body('content')
    #: Template variable list.
    tag_names = resource.Body('tag_names', type=list)
    #: Time when the template was created.
    #:  The UTC time is in YYYY-MM-DDTHH:MM:SSZ format.
    create_time = resource.Body('create_time')
    #: Last time when the template was updated.
    #:  The UTC time is in YYYY-MM-DDTHH:MM:SSZ format.
    update_time = resource.Body('update_time')
    #: Request ID, which is unique.
    request_id = resource.Body('request_id')
