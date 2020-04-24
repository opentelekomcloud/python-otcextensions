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
'''DMS Instance v1 action implementations'''
from osc_lib import exceptions
from osc_lib import utils
from osc_lib.command import command

from otcextensions.common import sdk_utils
from otcextensions.i18n import _


INSTANCE_STATUS_CHOICES = ['CREATING', 'CREATEFAILED', 'RUNNING', 'ERROR',
                           'STARTING', 'RESTARTING', 'CLOSING', 'FROZEN']
RETENTION_POLICY_CHOICES = ['produce_reject', 'time_base']
STORAGE_SPEC_CHOICES = ['dms.physical.storage.high',
                        'dms.physical.storage.ultra']


def _get_columns(item):
    column_map = {}
    hidden = ['location']
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map,
                                                           hidden)


class ListDMSInstance(command.Lister):
    _description = _('List DMS Instances')
    columns = ('ID', 'name', 'engine_name', 'engine_version',
               'storage_spec_code', 'status', 'connect_address', 'router_id',
               'network_id', 'security_group_id', 'user_name', 'storage',
               'total_storage', 'used_storage')

    def get_parser(self, prog_name):
        parser = super(ListDMSInstance, self).get_parser(prog_name)

        parser.add_argument(
            '--engine-name',
            metavar='<engine>',
            help=_('Engine name')
        )

        parser.add_argument(
            '--status',
            metavar='{' + ','.join(INSTANCE_STATUS_CHOICES) + '}',
            type=lambda s: s.upper(),
            choices=INSTANCE_STATUS_CHOICES,
            help=_('Instance status')
        )

        parser.add_argument(
            '--include-failure',
            action='store_true',
            help=_('Include instances failed to create')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        query_params = {}
        for param in ['engine_name', 'status', 'include_failure']:
            val = getattr(parsed_args, param)
            if val is not None:
                query_params[param] = val

        data = client.instances(**query_params)

        table = (self.columns,
                 (utils.get_item_properties(
                     s, self.columns,
                 ) for s in data))
        return table


class ShowDMSInstance(command.ShowOne):
    _description = _('Show single Instance details')

    def get_parser(self, prog_name):
        parser = super(ShowDMSInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID of the instance')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        obj = client.find_instance(parsed_args.instance)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class DeleteDMSInstance(command.Command):
    _description = _('Delete DMS Instance')

    def get_parser(self, prog_name):
        parser = super(DeleteDMSInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            nargs='+',
            help=_('ID of the Instance')
        )
        return parser

    def take_action(self, parsed_args):

        if parsed_args.instance:
            client = self.app.client_manager.dms
            for instance in parsed_args.instance:
                client.delete_instance(instance)


class CreateDMSInstance(command.ShowOne):
    _description = _('Create DMS Instance')

    def get_parser(self, prog_name):
        parser = super(CreateDMSInstance, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of the instance.')
        )

        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('Description of the instance.')
        )
        parser.add_argument(
            '--engine-name',
            metavar='<engine>',
            help=_('Engine name. Currently only Kafka is supported.')
        )
        parser.add_argument(
            '--engine-version',
            metavar='<engine-ver>',
            help=_('Engine version. Currently only "2.3.0" is supported.')
        )
        parser.add_argument(
            '--storage',
            metavar='<GB>',
            type=int,
            required=True,
            help=_('Indicates the message storage space with increments '
                   'of 100 GB:\n'
                   'Instance with specification being 100MB: 600–90,000 GB\n'
                   'Instance with specification being 300MB: 1,200–90,000 GB\n'
                   'Instance with specification being 600MB: 2,400–90,000 GB\n'
                   'Instance with specification being 1200MB: 4,800–90,000 GB')
        )
        parser.add_argument(
            '--access-user',
            metavar='<access_user>',
            help=_(
                'This parameter is mandatory when engine is set to kafka and '
                'ssl_enable is set to true. This parameter is invalid when '
                'ssl_enable is set to false.\n'
                'Indicates a username. A username consists of 4 to 64 '
                'characters and supports only letters, digits, hyphens (-), '
                'and underscores (_).')
        )
        parser.add_argument(
            '--password',
            metavar='<password>',
            help=_(
                'This parameter is mandatory when engine is set to kafka and '
                'ssl_enable is set to true. This parameter is invalid when '
                'ssl_enable is set to false.\n'
                'An instance password must meet the following complexity '
                'requirements: \n'
                '- Must be a string consisting of 8 to 32 characters.\n'
                '- Must contain at least two of the following character '
                'types: \n'
                '-- Lowercase letters\n'
                '-- Uppercase letters\n'
                '-- Digits\n'
                '-- Special characters'
            )
        )
        parser.add_argument(
            '--router',
            metavar='<router>',
            required=True,
            help=_('Router ID or Name')
        )
        parser.add_argument(
            '--security-group',
            metavar='<sg>',
            required=True,
            help=_('Security group ID or Name')
        )
        parser.add_argument(
            '--network',
            metavar='<net>',
            required=True,
            help=_('Neutron network ID or Name')
        )
        parser.add_argument(
            '--availability-zone',
            metavar='<AZ>',
            required=True,
            action='append',
            help=_('List of availability zones')
        )
        parser.add_argument(
            '--product-id',
            metavar='<product>',
            required=True,
            help=_('Product ID of the DMS instance')
        )
        parser.add_argument(
            '--maintenance-begin',
            metavar='<HH24:MM>',
            help=_('Start of the instance maintenance window')
        )
        parser.add_argument(
            '--maintenance-end',
            metavar='<HH24:MM>',
            help=_('End of the instance maintenance window')
        )
        parser.add_argument(
            '--enable-public-access',
            action='store_true',
            help=_('Assign public ip to the instance')
        )
        parser.add_argument(
            '--enable-ssl',
            action='store_true',
            help=_('Enable SSL for the public access')
        )
        parser.add_argument(
            '--public-bandwidth',
            metavar='<Mbit/s>',
            type=int,
            help=_('Public network bandwidth in Mbit/s:\n'
                   'When specification 100MB: 3-900\n'
                   'When 300MB: 3-900\n'
                   'When 600MB: 4-1200\n'
                   'When 1200MB: 8-2400')
        )
        parser.add_argument(
            '--retention-policy',
            metavar='{' + ','.join(RETENTION_POLICY_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=RETENTION_POLICY_CHOICES,
            help=_('Action to be taken when the memory usage reaches the '
                   'disk capacity threshold. Options:\n'
                   ' `produce_reject`: New messages cannot be created.\n'
                   ' `time_base`: The earliest messages are deleted.')
        )
        parser.add_argument(
            '--storage-spec-code',
            metavar='{' + ','.join(STORAGE_SPEC_CHOICES) + '}',
            type=lambda s: s.lower(),
            choices=STORAGE_SPEC_CHOICES,
            help=_('The storage I/O specification of a Kafka instance.\n'
                   'When specification is 100MB, the storage I/O can be:'
                   '[`dms.physical.storage.high`, '
                   '`dms.physical.storage.ultra`]\n'
                   'When specification is 300MB, the storage I/O can be:'
                   '[`dms.physical.storage.high`, '
                   '`dms.physical.storage.ultra`]\n'
                   'When specification is 600MB, the storage I/O is '
                   '`dms.physical.storage.ultra`.\n'
                   'When specification is 1200MB, the storage I/O is '
                   '`dms.physical.storage.ultra`.')
        )

        return parser

    def take_action(self, parsed_args):

        attrs = {}

        attrs['name'] = parsed_args.name
        for attr in ['description', 'engine_name', 'engine_version', 'storage',
                     'access_user', 'password', 'product_id',
                     'maintenance_begin', 'maintenance_end',
                     'public_bandwidth',
                     'retention_policy', 'storage_spec_code']:
            val = getattr(parsed_args, attr)
            if val is not None:
                attrs[attr] = val

        network_client = self.app.client_manager.network

        router_obj = network_client.find_router(parsed_args.router,
                                                ignore_missing=False)
        attrs['router_id'] = router_obj.id
        net_obj = network_client.find_network(parsed_args.network,
                                              ignore_missing=False)
        attrs['network_id'] = net_obj.id
        sg_obj = self.app.client_manager.compute.find_security_group(
            parsed_args.security_group, ignore_missing=False)
        attrs['security_group_id'] = sg_obj.id

        if parsed_args.availability_zone:
            attrs['availability_zone'] = parsed_args.availability_zone

        if parsed_args.maintenance_begin and parsed_args.maintenance_end:
            attrs['maintenance_begin'] = parsed_args.maintenance_begin
            attrs['maintenance_end'] = parsed_args.maintenance_end
        elif parsed_args.maintenance_begin or parsed_args.maintenance_end:
            raise exceptions.CommandException(_(
                '`maintenance_start` and `maintenance_end` can be set only'
                'together'))
        if parsed_args.enable_public_access:
            attrs['is_public'] = True
            if parsed_args.enable_ssl:
                attrs['is_ssl'] = True

        client = self.app.client_manager.dms

        obj = client.create_instance(**attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class UpdateDMSInstance(command.ShowOne):
    _description = _('Update DMS Instance')

    def get_parser(self, prog_name):
        parser = super(UpdateDMSInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<inst>',
            help=_('Name or ID of the DMS instance')
        )
        parser.add_argument(
            '--name',
            metavar='<name>',
            help=_('New name of the instance.')
        )
        parser.add_argument(
            '--description',
            metavar='<description>',
            help=_('New description of the instance.')
        )
        parser.add_argument(
            '--security-group',
            metavar='<sg>',
            required=True,
            help=_('Security group ID or Name')
        )
        parser.add_argument(
            '--maintenance-begin',
            metavar='<HH24:MM>',
            help=_('Start of the instance maintenance window')
        )
        parser.add_argument(
            '--maintenance-end',
            metavar='<HH24:MM>',
            help=_('End of the instance maintenance window')
        )
        return parser

    def take_action(self, parsed_args):

        attrs = {}

        attrs['name'] = parsed_args.name
        for attr in ['description', 'maintenance_begin', 'maintenance_end']:
            val = getattr(parsed_args, attr)
            if val is not None:
                attrs[attr] = val

        sg_obj = self.app.client_manager.compute.find_security_group(
            parsed_args.security_group, ignore_missing=False)
        attrs['security_group_id'] = sg_obj.id

        if parsed_args.maintenance_begin and parsed_args.maintenance_end:
            attrs['maintenance_begin'] = parsed_args.maintenance_begin
            attrs['maintenance_end'] = parsed_args.maintenance_end
        elif parsed_args.maintenance_begin or parsed_args.maintenance_end:
            raise exceptions.CommandException(_(
                '`maintenance_start` and `maintenance_end` can be set only'
                'together'))

        client = self.app.client_manager.dms

        instance = client.find_instance(parsed_args.instance,
                                        ignore_missing=False)

        obj = client.update_instance(instance, **attrs)

        display_columns, columns = _get_columns(obj)
        data = utils.get_item_properties(obj, columns)

        return (display_columns, data)


class RestartDMSInstance(command.Command):
    _description = _('Restart single Instance')

    def get_parser(self, prog_name):
        parser = super(RestartDMSInstance, self).get_parser(prog_name)
        parser.add_argument(
            'instance',
            metavar='<instance>',
            help=_('ID of the instance')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.dms

        obj = client.find_instance(parsed_args.instance, ignore_missing=False)

        client.restart_instance(obj)

        return
