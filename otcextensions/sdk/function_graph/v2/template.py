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


class TriggerMetadataList(resource.Resource):
    trigger_name = resource.Body('trigger_name', type=str)
    trigger_type = resource.Body('trigger_type', type=str)
    event_type = resource.Body('event_type', type=str)
    event_data = resource.Body('event_data', type=str)


class TempDetail(resource.Resource):
    input = resource.Body('input', type=str)
    output = resource.Body('output', type=str)
    warning = resource.Body('warning', type=str)


class Template(resource.Resource):
    base_path = 'fgs/templates/%(template_id)s'
    # Capabilities
    allow_fetch = True
    # Properties
    template_id = resource.URI('template_id', type=str)

    # Attributes
    #: Template ID.
    id = resource.Body('id', type=str)
    #: Template type.
    type = resource.Body('type', type=int)
    #: Template title.
    title = resource.Body('title', type=str)
    #: Template name.
    template_name = resource.Body('template_name', type=str)
    #: Template description.
    description = resource.Body('description', type=str)
    #: Template runtime.
    runtime = resource.Body('runtime', type=str)
    #: Template handler.
    handler = resource.Body('handler', type=str)
    #: Code type.
    code_type = resource.Body('code_type', type=str)
    #: Code file.
    code = resource.Body('code', type=str)
    #: Maximum duration the function can be executed.
    #: Value range: 3s-259,200s.
    timeout = resource.Body('timeout', type=int)
    #: Memory size.
    memory_size = resource.Body('memory_size', type=int)
    #: Trigger information.
    trigger_metadata_list = resource.Body(
        'trigger_metadata_list', type=list, list_type=TriggerMetadataList)
    #: Template details.
    temp_detail = resource.Body('temp_detail', type=TempDetail)
    #: User data.
    user_data = resource.Body('user_data', type=str)
    #: Encrypted user data.
    encrypted_user_data = resource.Body('encrypted_user_data', type=str)
    #: Dependencies required by the template.
    dependencies = resource.Body('dependencies', type=list)
    #: Template application scenarios.
    scene = resource.Body('scene', type=str)
    #: Cloud service associated with the template.
    service = resource.Body('service', type=str)
