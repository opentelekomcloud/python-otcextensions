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


class Image(resource.Resource):
    resource_key = 'image'
    base_path = '/cloudimages/action'

    allow_create = True
    #: Method for creating a resource (POST, PUT)
    create_method = "POST"

    name = resource.Body('name')
    description = resource.Body('description')
    os_type = resource.Body('os_type')
    os_version = resource.Body('os_version')
    image_url = resource.Body('image_url')
    min_disk = resource.Body('min_disk', type=int)
    is_config = resource.Body('is_config', type=bool)
    cmk_id = resource.Body('cmk_id')
    type = resource.Body('type')
    enterprise_project_id = resource.Body('enterprise_project_id')
    max_ram = resource.Body('max_ram', type=int)
    min_ram = resource.Body('min_ram', type=int)
    is_quick_import = resource.Body('is_quick_import', type=bool)
    tags = resource.Body('tags', type=list)
    image_tags = resource.Body('image_tags', type=list)
    data_images = resource.Body('data_images', type=list)
