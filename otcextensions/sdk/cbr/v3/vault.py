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


class TagSpec (resource.Resource):
    #: Properties
    #: Tag key, up to 36 chars
    key = resource.Body('key')
    #: Tag value, up to 43 chars
    value= resourcde.Body('value')


class BindRuleSpec(resource.Resource):
    #: Properties
    #: Filters automatically associated resources by tag
    tags = resource.Body('tags', type=list, list_type=TagSpec)


class VolumeSpec(resource.Resource):
    #: Properties
    #: Volume id
    id = resource.Body('id')
    #: OS type
    os_version

class ResourceExtraInfoSpec(resource.Resource):
    #: Properties
    #: ID of the disk that is excluded from the backup
    exclude_volumes = resource.Body('exclude_volumes', type=list)
    #: Disk to be backed up
    include_volumes = resource.Body('include_volumes', type=list, 
                                    list_type=VolumeSpec)


class ResourceSpec(resource.Resource):
    #: Properties
    #: Extra info of the resource
    extra_info = resource.Body('extra_info', type=ResourceExtraInfoSpec)
    #: ID of the resource to be backed up
    id = resource.Body('id')
    #: Resource name
    name = resource.Body('name')
    #: type of the resource to be backed up.
    #: values: OS::Nova::Server, OS::Cinder::Volume
    type = resource.Body('type')


class BillingExtraInfoSpec(resource.Resource):
    #: Properties
    #: Number of items in the aplication for creating vaults in the
    #: combination mode
    combined_order_ecs_num = resource.Body('combined_order_ecs_num')
    #: ID of the application for creating vaults in combination
    combined_order_id = resource.Body('combined_order_id')


class BillingSpec(resource.Resource):
    #: Properties
    #: Biling mode
    #: values: post_paid, pre_paid
    #: default: post_paid
    charging_mode = resource.Body('charging_mode')
    #: Cloud platform
    #: values: public, hybrid
    cloud_type = resource.Body('cloud_type')
    #: Backup specifications
    #: default: crash_consistent
    consistent_level = resource.Body('consistent_level')
    #: Redirection URL
    console_url = resource.Body('console_url')
    #: Billing extra info spec
    extra_info = resource.Body('extra_info', type=BillingExtraInfoSpec)
    #: Whether the fee is automatically deducted from the customers account
    #: default: false
    is_auto_pay = resource.Body('is_auto_pay', type=bool)
    #: Whether to automatically renew the subscirption after expiration
    #: default: false
    is_auto_renew = resource.Body('is_auto_renew', type=bool)
    #: Object type
    object_type = resource.Body('object_type')
    #: Required duration for the package
    #: mandatory if charging_mode is set to pre_paid
    period_num = resource.Body('period_num', type=int)
    #: Package type
    #: mandatory if charging_mode is pre_paid
    #: values: year, month
    period_type = resource.Body('period_type')
    #: Operation type
    protect_type = resource.Body('operation_type')
    #: Capicity in GB
    #: min: 1, max: 10485760
    size = resource.Body('size', type=int)



class Vault(resource.Resource):
    """CBR Vault Resource"""
    resource_key = 'backup'
    resources_key = 'backups'
    base_path = '/vaults'

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'cloud_type', 'enterprise_project_id', 'id', 'limit',
        'name', 'object_type', 'offset', 'policy_id', 'protect_type',
        'resources_ids', 'status')

    #: Properties
    auto_bind = resource.Body('auto_bind', type=bool)
    #: Whether to automatically expand the vault capacity
    auto_expand = resource.Body('auto_expand', type=bool)
    #: Backup Policy ID
    backup_policy_id = resource.Body('backup_policy_id')
    #: Billing spec
    billing = resource.Body('billing', type=BillingSpec)
    #: Rules for automatic association
    bind_rules = resource.Body('bind_rules', type=BindRuleSpec)
    #: Description
    description = resource.Body('description')
    #: Enterprise project id
    #: default:0
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Vault name
    name = resource.Body('name')
    #: Associated Resources
    resources = resource.Body('resources', type=ResourceSpec)
    #: Tag list up to 10 key value pairs
    tags = resource.Body('tags', type=TagSpec)