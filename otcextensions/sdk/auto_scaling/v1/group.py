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

from otcextensions.sdk.auto_scaling.v1 import _base


class Group(_base.Resource):
    resource_key = 'scaling_group'
    resources_key = 'scaling_groups'
    base_path = '/scaling_group'
    query_marker_key = 'start_number'
    # service = auto_scaling_service.AutoScalingService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_fetch = True
    allow_delete = True
    allow_commit = True

    _query_mapping = resource.QueryParameters(
        'id', 'name', 'limit', 'marker',
        'scaling_configuration_id',
        name='scaling_group_name',
        status='scaling_group_status',
        marker=query_marker_key
    )

    #: Properties
    #: AutoScaling group ID
    id = resource.Body('scaling_group_id', alternate_id=True)
    #: AutoScaling group name
    name = resource.Body('scaling_group_name')
    #: AutoScaling group status,
    #: valid valus includes: ``INSERVICE``, ``PAUSED``, ``ERROR``
    status = resource.Body('scaling_group_status')
    #: AutoScaling group scaling status, *Type: bool*
    is_scaling = resource.Body('is_scaling', type=bool)
    #: AutoScaling group detail
    detail = resource.Body('detail')
    #: VPC id - (Router Id)
    router_id = resource.Body('vpc_id')
    #: network id list - (Subnet)
    networks = resource.Body('networks', type=list)
    #: security group id list
    security_groups = resource.Body('security_groups', type=list)
    #: Auto Scaling Config ID reference, used for creating instance
    scaling_configuration_id = resource.Body('scaling_configuration_id')
    #: Auto Scaling Config name
    scaling_configuration_name = resource.Body('scaling_configuration_name')
    #: Current alive instance number
    current_instance_number = resource.Body('current_instance_number')
    #: Desire alive instance number
    desire_instance_number = resource.Body('desire_instance_number')
    #: min alive instance number
    min_instance_number = resource.Body('min_instance_number')
    #: max alive instance number
    max_instance_number = resource.Body('max_instance_number')
    #: CoolDown time, only work with `ALARM` policy.
    #: default is 900, valid range is 0-86400
    cool_down_time = resource.Body('cool_down_time')
    #: load balancer listener id reference
    lb_listener_id = resource.Body('lb_listener_id')
    #: list of enhanced load balancers
    lbaas_listeners = resource.Body('lbaas_listeners')
    #: Health periodic audit method, Valid values include: ``ELB_AUDIT``,
    #: ``NOVA_AUDIT``, ELB_AUDIT and lb_listener_id are used in pairs.
    health_periodic_audit_method = resource.Body(
        'health_periodic_audit_method')
    #: Health periodic audit time, valid values include: ``5``, ``15``,
    #: ``60``, ``180``, default is ``5`` minutes
    health_periodic_audit_time = resource.Body('health_periodic_audit_time')
    #: Grace period for instance health check, valid if audit method is
    #: ``ELB_AUDIT``, value range is 0-86400, default value is 600
    health_periodic_audit_grace_period = \
        resource.Body('health_periodic_audit_grace_period')
    #: Instance terminate policy, valid values include:
    #: ``OLD_CONFIG_OLD_INSTANCE`` (default), ``OLD_CONFIG_NEW_INSTANCE``,
    #: ``OLD_INSTANCE``, ``NEW_INSTANCE``
    instance_terminate_policy = resource.Body('instance_terminate_policy')
    #: Notification methods, ``EMAIL``
    notifications = resource.Body('notifications')
    #: Should delete public ip when terminate instance, default ``false``
    delete_publicip = resource.Body('delete_publicip', type=bool)
    #: Should delete data disks when deleting the ECS, default ``false``
    delete_volume = resource.Body('delete_volume', type=bool)
    #: Availability zones
    availability_zones = resource.Body('available_zones')
    #: Enterprise project ID to which the AS group belongs
    enterprise_project_id = resource.Body('enterprise_project_id')
    #: Create time of the group
    create_time = resource.Body('create_time')
    #: The priority policy used to select target AZs, valid values include:
    #: ``EQUILIBRIUM_DISTRIBUTE`` (default), ``PICK_FIRST``
    multi_az_priority_policy = resource.Body('multi_az_priority_policy')

    def resume(self, session):
        '''resume group'''
        body = {'action': 'resume'}
        self._action(session, body)

    def pause(self, session):
        '''pause group'''
        body = {'action': 'pause'}
        self._action(session, body)
