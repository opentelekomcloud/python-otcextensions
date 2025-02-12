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
from openstack import utils
from openstack import exceptions


class Image(resource.Resource):
    resources_key = 'images'
    resource_key = 'image'
    base_path = '/cloudimages'

    allow_create = True
    allow_list = True
    allow_delete = True
    allow_commit = True

    #: Method for creating a resource (POST, PUT)
    create_method = "POST"
    commit_method = "PATCH"

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
    description = resource.Body('__description')
    os_type = resource.Body('os_type')
    os_version = resource.Body('__os_version')
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
    virtual_size = resource.Body('virtual_size')
    hw_firmware_type = resource.Body('hw_firmware_type')
    disk_format = resource.Body('disk_format')
    container_format = resource.Body('container_format')
    hw_vif_multiqueue_enabled = resource.Body('hw_vif_multiqueue_enabled')
    checksum = resource.Body('checksum')
    size = resource.Body('size')
    file = resource.Body('file')
    os_bit = resource.Body('__os_bit')
    platform = resource.Body('__platform')
    is_registered = resource.Body('__is_registered')
    os_type = resource.Body('__os_type')
    image_source_type = resource.Body('__image_source_type')
    imagetype = resource.Body('__imagetype')
    originalimagename = resource.Body('__originalimagename')
    backup_id = resource.Body('__backup_id')
    productcode = resource.Body('__productcode')
    image_size = resource.Body('__image_size')
    support_fc_inject = resource.Body('__support_fc_inject')
    data_origin = resource.Body('__data_origin')


    def create(self, session, prepend_key=False, base_path=None):
        # Overriden here to override prepend_key default value
        return super(Image, self).create(session, prepend_key, base_path
                                         + '/action')
    
    def _action(self, session, request_body, image_id):
        url = utils.urljoin(self.base_path, image_id)
        response = session.patch(url, json=request_body)
        exceptions.raise_from_response(response)
        return response

    def update_image_details(self, session, image_id, command_list):
        request_body = command_list
        response = self._action(session=session, request_body=request_body, image_id=image_id)
        return self._to_object(session, response)     

    def _to_object(self, session, response):
        has_body = (
            self.has_body
            if self.create_returns_body is None
            else self.create_returns_body
        )
        microversion = self._get_microversion(session, action='create')
        self.microversion = microversion
        self._translate_response(response, has_body=has_body)
        if self.has_body and self.create_returns_body is False:
            return self.fetch(session)
        return self
