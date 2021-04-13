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


class TagSpec (resource.Resource):
    #: Properties
    #: Tag key, up to 36 chars
    key = resource.Body('key')
    #: Tag value, up to 43 chars
    value = resource.Body('value')


class BindRuleSpec(resource.Resource):
    #: Properties
    #: Filters automatically associated resources by tag
    tags = resource.Body('tags', type=list, list_type=TagSpec)


class VolumeSpec(resource.Resource):
    #: Properties
    #: Volume id
    id = resource.Body('id')
    #: OS type
    os_version = resource.Body('os_version')


class ResourceExtraInfoSpec(resource.Resource):
    #: Properties
    #: ID of the disk that is excluded from the backup
    exclude_volumes = resource.Body('exclude_volumes', type=list)
    #: Disk to be backed up
    include_volumes = resource.Body('include_volumes', type=list,
                                    list_type=VolumeSpec)


class ResourceSpec(resource.Resource):
    #: Properties
    #: Number of backups
    backup_count = resource.Body('backup_count', type=int)
    #: Backup size
    backup_size = resource.Body('backup_size', type=int)
    #: Extra info of the resource
    extra_info = resource.Body('extra_info', type=ResourceExtraInfoSpec)
    #: ID of the resource to be backed up
    id = resource.Body('id')
    #: Resource name
    name = resource.Body('name')
    #: Protection status
    #: values: available, error, protecting, restoring, removing
    protect_status = resource.Body('protect_status')
    #: Allocated capacity for the associated resource, in GB
    size = resource.Body('size', type=int)
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
    #: Allocated capacity in MB
    allocated = resource.Body('allocated', type=int)
    #: Biling mode
    #: values: post_paid, pre_paid
    #: default: post_paid
    charging_mode = resource.Body('charging_mode')
    #: Cloud type
    #: values: public, hybrid
    cloud_type = resource.Body('cloud_type')
    #: Backup specifications
    #: default: crash_consistent
    consistent_level = resource.Body('consistent_level')
    #: Redirection URL
    console_url = resource.Body('console_url')
    #: Billing extra info spec
    extra_info = resource.Body('extra_info', type=BillingExtraInfoSpec)
    #: Scenario when an account is frozen
    frozen_scene = resource.Body('frozen_scene')
    #: Whether the fee is automatically deducted from the customers account
    #: default: false
    is_auto_pay = resource.Body('is_auto_pay', type=bool)
    #: Whether to automatically renew the subscirption after expiration
    #: default: false
    is_auto_renew = resource.Body('is_auto_renew', type=bool)
    #: Object type
    object_type = resource.Body('object_type')
    #: Order ID
    order_id = resource.Body('order_id')
    #: Required duration for the package
    #: mandatory if charging_mode is set to pre_paid
    period_num = resource.Body('period_num', type=int)
    #: Package type
    #: mandatory if charging_mode is pre_paid
    #: values: year, month
    period_type = resource.Body('period_type')
    #: Product ID
    product_id = resource.Body('product_id')
    #: Operation type
    protect_type = resource.Body('operation_type')
    #: Capicity in GB
    #: min: 1, max: 10485760
    size = resource.Body('size', type=int)
    #: Specification code
    spec_code = resource.Body('spec_code')
    #: Status
    #: values: available, lock, frozen, deleting, error
    status = resource.Body('status')
    #: Name of the bucket of the vault
    storage_unit = resource.Body('storage_unit')
    #: Used capacity in MB
    used = resource.Body('used', type=int)


class Vault(resource.Resource):
    """CBR Vault Resource"""
    resource_key = 'vault'
    resources_key = 'vaults'
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
    #: Creation time
    created_at = resource.Body('created_at')
    #: Description
    description = resource.Body('description')
    #: Enterprise project id
    #: default:0
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Vault name
    name = resource.Body('name')
    #: Project ID
    project_id = resource.Body('project_id')
    #: Vault type
    provider_id = resource.Body('provider_id')
    #: Associated Resources
    resources = resource.Body('resources', type=ResourceSpec)
    #: Tag list up to 10 key value pairs
    tags = resource.Body('tags', type=TagSpec)
    #: User ID
    user_id = resource.Body('user_id')

    def bind_policy(self, session, policy_id):
        """Method to associate a CBR policy to a CBR vault

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str policy_id: The ID of the policy being attached to the
            CBR vault.
        """
        url = utils.urljoin(self.base_path, self.id, 'associatepolicy')
        body = {
            'policy_id': policy_id
        }
        return session.post(url, json=body)

    def unbind_policy(self, session, policy_id):
        """Method to dissociate a CBR policy from a CBR vault

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param str policy_id: The ID of the policy being attached to the
            CBR vault.
        """
        url = utils.urljoin(self.base_path, self.id, 'dissociatepolicy')
        body = {
            'policy_id': policy_id
        }
        return session.post(url, json=body)

    def associate_resources(self, session, resources):
        """Method to bind one or more ECS or Volume to a CBR vault

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param resources: array of resources in the format, while param id
            and type are mandatory:
            resources = [{
                'id' : <resource_id>,
                'type' : '<OS::Nova::Server|OS::Cinder::Volume>'
                'extra_info': {
                    'include_volumes': [
                        <None|array_of_volume_ids>
                    ],
                    'exclude_volumes': [
                        '<None|array_of_volume_ids>']
                },
            }]
        """
        url = utils.urljoin(self.base_path, self.id, 'addresources')
        body = {
            'resources': resources
        }
        return session.post(url, json=body)

    def dissociate_resources(self, session, resources):
        """Method to release one or more ECS or Volume to a CBR vault

        :param session: The session to use for making this request.
        :type session: :class:`~keystoneauth1.adapter.Adapter`
        :param resources: list of ressource ids to be released from vault
        """
        url = utils.urljoin(self.base_path, self.id, 'removeresources')
        body = {
            'resource_ids': resources
        }
        return session.post(url, json=body)
