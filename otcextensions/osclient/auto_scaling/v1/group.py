#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
"""AS Groups v1 action implementations"""

import logging

from osc_lib.command import command
from osc_lib import utils

from otcextensions.i18n import _

from otcextensions.common import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def set_attributes_for_print_detail(obj):
    info = {}  # instance._info.copy()
    info['name'] = obj.name
    info['id'] = obj.id
    info['create_time'] = obj.create_time
    instance_config = obj.instance_config
    if instance_config:
        info['instance_name'] = instance_config.instance_name
        info['instance_id'] = instance_config.instance_id
        info['flavor_id'] = instance_config.flavor_id
        info['image_id'] = instance_config.image_id
        info['key_name'] = instance_config.key_name
        info['public_ip'] = instance_config.public_ip
        info['user_data'] = instance_config.user_data
        info['metadata'] = instance_config.metadata
        disks = []
        for disk in instance_config.disk:
            dsk = {
                'size': disk['size'],
                'volume_type': disk['volume_type'],
                'disk_type': disk['disk_type'],
            }
            disks.append(dsk)
        info['disk'] = disks

    return info


class ListAutoScalingGroup(command.Lister):
    _description = _('List AutoScaling Groups')
    columns = ('ID', 'Name', 'status', 'detail')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed')
        )
        parser.add_argument(
            '--marker',
            dest='marker',
            metavar='<ID>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        data = client.groups()

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowAutoScalingGroup(command.ShowOne):
    _description = _('Shows details of a AutoScalinig group')
    columns = ['ID', 'Name', 'Status', 'Detail',
               'scaling_configuration_id', 'scaling_configuration_name',
               'current_instance_number', 'desire_instance_number',
               'min_instance_number', 'max_instance_number',
               'cool_down_time', 'networks', 'available_zones',
               'security_group']

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'group',
            metavar='<group>',
            help=_('ID or name of the configuration group')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        obj = client.find_group(parsed_args.group, ignore_missing=False)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns, formatters={})

        return (display_columns, data)


class CreateAutoScalingGroup(command.ShowOne):
    _description = _('Creates AutoScalinig group')
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the new configuration group')
        )
        parser.add_argument(
            '--desire_instance_number',
            metavar='<desire_instance_number>',
            type=int,
            help=_('Desired number of instances')
        )
        parser.add_argument(
            '--min_instance_number',
            metavar='<min_instance_number>',
            type=int,
            help=_('Minimal number of instances')
        )
        parser.add_argument(
            '--max_instance_number',
            metavar='<max_instance_number>',
            type=int,
            help=_('Maximal number of instances')
        )
        parser.add_argument(
            '--cool_down_time',
            metavar='<cool_down_time>',
            type=int,
            help=_('Specifies cooling duration in seconds')
        )
        parser.add_argument(
            '--lb_listener_id',
            metavar='<lb_listener_id>',
            help=_('Specifies ELB Listener ID')
        )
        parser.add_argument(
            '--lbaas_listener',
            metavar='<lbaas_listener>',
            action='append',
            help=_('Specifies ULB Listener Information in format: '
                   'ID:PORT:Weight(optional) '
                   '(Repeat multiple times, up to 3 times)')
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            action='append',
            help=_('Specifies the availability zones information '
                   '(Repeat multiple times)')
        )
        parser.add_argument(
            '--subnetwork',
            metavar='<subnetwork_id>',
            action='append',
            required=True,
            help=_('Network ID of the subnet'
                   '(Repeat multiple times, up to 5 times)')
        )
        parser.add_argument(
            '--security_group',
            metavar='<security_group>',
            action='append',
            required=True,
            help=_('Security Group ID'
                   '(Repeat multiple times)')
        )
        parser.add_argument(
            '--network_id',
            metavar='<network_id>',
            required=True,
            help=_('Network (VPC) ID')
        )
        parser.add_argument(
            '--audit_method',
            metavar='<audit_method>',
            help=_('Specifies the audit method [`NOVA_AUDIT`, `ELB_AUDIT`]')
        )
        parser.add_argument(
            '--audit_time',
            metavar='<audit_time>',
            type=int,
            help=_('Specifies the audit time in minutes')
        )
        parser.add_argument(
            '--terminate_policy',
            metavar='<terminate_policy>',
            help=_('Specifies the termination policy'
                   ' [`OLD_CONFIG_OLD_INSTANCE` (default), '
                   '`OLD_CONFIG_NEW_INSTANCE`, '
                   '`OLD_INSTANCE`, '
                   '`NEW_INSTANCE`]')
        )
        parser.add_argument(
            '--notification',
            metavar='<notification>',
            action='append',
            help=_('Specifies the notification method (`EMAIL` for Email) '
                   '(Repeat multiple times)')
        )
        parser.add_argument(
            '--delete_public_ip',
            default=False,
            action='store_true',
            help=_('Specifies whether to delete EIP when deleting the ECS')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        args['name'] = parsed_args.name
        args['vpc_id'] = parsed_args.network_id

        subnets = []
        for subnet in parsed_args.subnetwork:
            subnets.append({'id': subnet})
        args['networks'] = subnets

        sgs = []
        for sg in parsed_args.security_group:
            sgs.append({'id': sg})
        args['security_groups'] = sgs

        if parsed_args.desire_instance_number:
            args['desire_instance_number'] = parsed_args.desire_instance_number
        if parsed_args.max_instance_number:
            args['max_instance_number'] = parsed_args.max_instance_number
        if parsed_args.min_instance_number:
            args['min_instance_number'] = parsed_args.min_instance_number
        if parsed_args.cool_down_time:
            args['cool_down_time'] = parsed_args.cool_down_time
        if parsed_args.lb_listener_id:
            args['lb_listener_id'] = parsed_args.lb_listener_id
        if parsed_args.lbaas_listener:
            listeners = []
            for lsnr in parsed_args.lbaas_listener:
                lb_parts = lsnr.split(':')
                lb = {
                    'id': lb_parts[0],
                    'protocol_port': lb_parts[1]
                }
                if len(lb_parts) == 3:
                    lb['weight'] = lb_parts[2]
                listeners.append(lb)
            args['lbaas_listeners'] = listeners
        if parsed_args.availability_zone:
            zones = []
            for zone in parsed_args.availability_zone:
                zones.append(zone)
            # zones.append(zone for zone in parsed_args.availability_zone)
            args['available_zones'] = zones
        if parsed_args.audit_method:
            args['health_periodic_audit_method'] = parsed_args.audit_method
        if parsed_args.audit_time:
            args['health_periodic_audit_time'] = parsed_args.audit_time
        if parsed_args.terminate_policy:
            args['instance_terminate_policy'] = parsed_args.terminate_policy
        if parsed_args.delete_public_ip:
            args['delete_public_ip'] = parsed_args.delete_public_ip
        if parsed_args.notification:
            lst = []
            for notification in parsed_args.notification:
                lst.append(notification)
            args['notifications'] = lst

        client = self.app.client_manager.auto_scaling
        group = client.create_group(**args)
        display_columns, columns = _get_columns(group)
        data = utils.get_item_properties(group, columns, formatters={})

        return (display_columns, data)


class DeleteAutoScalingGroup(command.Command):
    _description = _('Deletes AutoScalinig group')
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'group',
            metavar='<group>',
            help=_('ID or name of the configuration group to be deleted')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling
        if parsed_args.group:
            client.delete_group(parsed_args.group, ignore_missing=False)


class UpdateAutoScalingGroup(command.ShowOne):
    _description = _('Updates AutoScalinig group')

    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(UpdateAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'group',
            metavar='<group>',
            help=_('AS Group name or ID')
        )
        parser.add_argument(
            '--desire_instance_number',
            metavar='<desire_instance_number>',
            type=int,
            help=_('Desired number of instances')
        )
        parser.add_argument(
            '--min_instance_number',
            metavar='<min_instance_number>',
            type=int,
            help=_('Minimal number of instances')
        )
        parser.add_argument(
            '--max_instance_number',
            metavar='<max_instance_number>',
            type=int,
            help=_('Maximal number of instances')
        )
        parser.add_argument(
            '--cool_down_time',
            metavar='<cool_down_time>',
            type=int,
            help=_('Specifies cooling duration in seconds')
        )
        parser.add_argument(
            '--lb_listener_id',
            metavar='<lb_listener_id>',
            help=_('Specifies ELB Listener ID')
        )
        parser.add_argument(
            '--lbaas_listener',
            metavar='<lbaas_listener>',
            action='append',
            help=_('Specifies ULB Listener Information in format: '
                   'ID:PORT:Weight(optional) '
                   '(Repeat multiple times, up to 3 times)')
        )
        parser.add_argument(
            '--availability_zone',
            metavar='<availability_zone>',
            action='append',
            help=_('Specifies the availability zones information '
                   '(Repeat multiple times)')
        )
        parser.add_argument(
            '--subnetwork',
            metavar='<subnetwork_id>',
            action='append',
            required=True,
            help=_('Network ID of the subnet'
                   '(Repeat multiple times, up to 5 times)')
        )
        parser.add_argument(
            '--security_group',
            metavar='<security_group>',
            action='append',
            required=True,
            help=_('Security Group ID'
                   '(Repeat multiple times)')
        )
        parser.add_argument(
            '--network_id',
            metavar='<network_id>',
            required=True,
            help=_('Network (VPC) ID')
        )
        parser.add_argument(
            '--audit_method',
            metavar='<audit_method>',
            help=_('Specifies the audit method [`NOVA_AUDIT`, `ELB_AUDIT`]')
        )
        parser.add_argument(
            '--audit_time',
            metavar='<audit_time>',
            type=int,
            help=_('Specifies the audit time in minutes')
        )
        parser.add_argument(
            '--terminate_policy',
            metavar='<terminate_policy>',
            help=_('Specifies the termination policy'
                   ' [`OLD_CONFIG_OLD_INSTANCE` (default), '
                   '`OLD_CONFIG_NEW_INSTANCE`, '
                   '`OLD_INSTANCE`, '
                   '`NEW_INSTANCE`]')
        )
        parser.add_argument(
            '--notification',
            metavar='<notification>',
            action='append',
            help=_('Specifies the notification method (`EMAIL` for Email) '
                   '(Repeat multiple times)')
        )
        parser.add_argument(
            '--delete_public_ip',
            default=False,
            action='store_true',
            help=_('Specifies whether to delete EIP when deleting the ECS')
        )
        return parser

    def take_action(self, parsed_args):

        args = {}
        args['vpc_id'] = parsed_args.network_id

        subnets = []
        for subnet in parsed_args.subnetwork:
            subnets.append({'id': subnet})
        args['networks'] = subnets

        sgs = []
        for sg in parsed_args.security_group:
            sgs.append({'id': sg})
        args['security_groups'] = sgs

        if parsed_args.desire_instance_number:
            args['desire_instance_number'] = parsed_args.desire_instance_number
        if parsed_args.max_instance_number:
            args['max_instance_number'] = parsed_args.max_instance_number
        if parsed_args.min_instance_number:
            args['min_instance_number'] = parsed_args.min_instance_number
        if parsed_args.cool_down_time:
            args['cool_down_time'] = parsed_args.cool_down_time
        if parsed_args.lb_listener_id:
            args['lb_listener_id'] = parsed_args.lb_listener_id
        if parsed_args.lbaas_listener:
            listeners = []
            for lsnr in parsed_args.lbaas_listener:
                lb_parts = lsnr.split(':')
                lb = {
                    'id': lb_parts[0],
                    'protocol_port': lb_parts[1]
                }
                if len(lb_parts) == 3:
                    lb['weight'] = lb_parts[2]
                listeners.append(lb)
            args['lbaas_listeners'] = listeners
        if parsed_args.availability_zone:
            zones = []
            for zone in parsed_args.availability_zone:
                zones.append(zone)
            # zones.append(zone for zone in parsed_args.availability_zone)
            args['available_zones'] = zones
        if parsed_args.audit_method:
            args['health_periodic_audit_method'] = parsed_args.audit_method
        if parsed_args.audit_time:
            args['health_periodic_audit_time'] = parsed_args.audit_time
        if parsed_args.terminate_policy:
            args['instance_terminate_policy'] = parsed_args.terminate_policy
        if parsed_args.delete_public_ip:
            args['delete_public_ip'] = parsed_args.delete_public_ip
        if parsed_args.notification:
            lst = []
            for notification in parsed_args.notification:
                lst.append(notification)
            args['notifications'] = lst

        client = self.app.client_manager.auto_scaling
        group = client.update_group(group=parsed_args.group, **args)
        display_columns, columns = _get_columns(group)
        data = utils.get_item_properties(group, columns, formatters={})

        return (display_columns, data)


class DisableAutoScalingGroup(command.Command):
    _description = _('Disable/pause AutoScalinig group')

    def get_parser(self, prog_name):
        parser = super(DisableAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'group',
            metavar='<group>',
            help=_('ID or name of the configuration group')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling
        if parsed_args.group:
            group = client.find_group(parsed_args.group, ignore_missing=False)
            self.app.client_manager.auto_scaling.pause_group(group)


class EnableAutoScalingGroup(command.Command):
    _description = _('Enable/resume AutoScalinig group')

    def get_parser(self, prog_name):
        parser = super(EnableAutoScalingGroup, self).get_parser(prog_name)
        parser.add_argument(
            'group',
            metavar='<group>',
            help=_('ID or name of the configuration group')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling
        if parsed_args.group:
            group = client.find_group(parsed_args.group, ignore_missing=False)
            self.app.client_manager.auto_scaling.resume_group(group)
