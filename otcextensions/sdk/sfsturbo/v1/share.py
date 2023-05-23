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


class Share(resource.Resource):

    base_path = '/sfs-turbo/shares'
    resource_key = 'share'
    resources_key = 'shares'

    # capabilities
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    #: Specifies the creation progress of the SFS Turbo file system.
    #: *Type: dict*
    action_progress = resource.Body('action_progress', type='dict')
    #: Specifies the name of the AZ where the SFS Turbo file system is located.
    #: *Type: str*
    az_name = resource.Body('az_name')
    #: Specifies the available capacity of the SFS Turbo file system in the
    # unit of GB.
    #: *Type: str*
    avail_capacity = resource.Body('avail_capacity')
    #: Specifies the code of the AZ where the SFS Turbo file system is located.
    #: *Type: str*
    availability_zone = resource.Body('availability_zone')
    #: Specifies the creation time.
    #: *Type: str*
    created_at = resource.Body('created_at')
    #: Specifies the ID of the encryption key specified by the user.
    # This parameter is not returned for non-encrypted disks.
    #: *Type: str*
    crypt_key_id = resource.Body('crypt_key_id')
    #: For an enhanced file system, bandwidth is returned for this field.
    #: *Type: str*
    expand_type = resource.Body('expand_type')
    #: Specifies the mount point of the SFS Turbo file system.
    #: *Type: str*
    export_location = resource.Body('export_location')
    #: Specifies the name of the SFS Turbo file system.
    #: *Type: str*
    name = resource.URI('name')
    #: Specifies the status of the SFS Turbo file system.
    #: *Type: str*
    status = resource.Body('instance_mode')
    #: Specifies the sub-status of the SFS Turbo file system.
    #: *Type:str*
    sub_status = resource.Body('sub_status')
    #: Specifies the type of the SFS Turbo file system.
    #: *Type: str*
    share_type = resource.Body('share_type')
    #: Specifies the region of the SFS Turbo file system.
    #: *Type: str*
    region = resource.Body('region')
    #: Specifies the network ID of the subnet specified by the user.
    #: *Type: str*
    subnet_id = resource.Body('subnet_id')
    #: Specifies the ID of a security group specified by the user.
    #: *Type: str*
    security_group_id = resource.Body('security_group_id')
    #: Specifies the total capacity of the SFS Turbo file system in the
    # unit of GB.
    #: *Type: str*
    size = resource.Body('size')
    #: Specifies the protocol type of the SFS Turbo file system.
    # The current value is NFS.
    #: *Type: str*
    share_proto = resource.Body('share_proto')
    #: Billing mode of the SFS Turbo file system.
    #: *Type: str*
    pay_model = resource.Body('pay_model')
    #: Project id.
    #: *Type: str*
    project_id = resource.URI('project_id')
    #: Specifies the version ID of the SFS Turbo file system.
    #: *Type:str*
    version = resource.Body('version')
    #: Specifies the VPC ID specified by the user.
    #: *Type: str*
    vpc_id = resource.Body('vpc_id')
