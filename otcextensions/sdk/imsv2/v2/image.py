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
    resources_key = 'images'
    resource_key = 'image'
    base_path = '/cloudimages'

    allow_create = True
    allow_list = True

    #: Method for creating a resource (POST, PUT)
    create_method = "POST"

    _query_mapping = resource.QueryParameters('limit', 'id',
                                              'name', 'status',
                                              '__isregistered',
                                              '__imagetype',
                                              '__whole_image',
                                              '__system__cmkid',
                                              'protected',
                                              'visibility',
                                              'owner',
                                              'container_format',
                                              'disk_format',
                                              'min_disk',
                                              'min_ram',
                                              '__os_bit',
                                              '__platform',
                                              'marker',
                                              'sort_key',
                                              'sort_dir',
                                              '__os_type',
                                              'tag',
                                              'member_status',
                                              '__support_kvm',
                                              '__support_xen',
                                              '__support_largememory',
                                              '__support_diskintensive',
                                              '__support_highperformance',
                                              '__support_xen_gpu_type',
                                              '__support_kvm_gpu_type',
                                              '__support_xen_hana',
                                              '__support_kvm_infiniband',
                                              'virtual_env_type',
                                              'enterprise_project_id')

    name = resource.Body('name')
    description = resource.Body('description')
    os_type = resource.Body('os_type')
    os_version = resource.Body('os_version')
    image_url = resource.Body('image_url')
    instance_id = resource.Body('instance_id')
    min_disk = resource.Body('min_disk', type=int)
    is_config = resource.Body('is_config', type=bool)
    cmk_id = resource.Body('cmk_id')
    type = resource.Body('type')
    max_ram = resource.Body('max_ram', type=int)
    min_ram = resource.Body('min_ram', type=int)
    is_quick_import = resource.Body('is_quick_import', type=bool)
    tags = resource.Body('tags', type=list)
    image_tags = resource.Body('image_tags', type=list)
    data_images = resource.Body('data_images', type=list)
    job_id = resource.Body('job_id')
    status = resource.Body('status')
    visibility = resource.Body('visibility')
    created_at = resource.Body('created_at')
    updated_at = resource.Body('updated_at')
    container_format = resource.Body('container_format')
    disk_format = resource.Body('disk_format')
    member_status = resource.Body('member_status')
    virtual_env_type = resource.Body('virtual_env_type')
    enterprise_project_id = resource.Body('enterprise_project_id')
    protected = resource.Body('protected', type=bool)

    def create(self, session, prepend_key=False, base_path=None):
        # Override here to override prepend_key default value
        return super(Image, self).create(session, prepend_key, base_path)
