#   Licensed under the Apache License, Version 2.0 (the 'License'); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#
'''AS Configurations v1 action implementations'''

import argparse
import base64
import logging

from osc_lib.command import command
from osc_lib import utils

from otcextensions.i18n import _

LOG = logging.getLogger(__name__)


def set_attributes_for_print_detail(obj):
    info = {}
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


class ListAutoScalingConfig(command.Lister):
    _description = _('List AutoScaling Configurations')
    columns = ('ID', 'Name')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingConfig, self).get_parser(prog_name)
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

        args = {}
        if parsed_args.limit:
            args['limit'] = parsed_args.limit
        if parsed_args.marker:
            args['marker'] = parsed_args.marker

        client = self.app.client_manager.auto_scaling

        data = client.configs(**args)

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowAutoScalingConfig(command.ShowOne):
    _description = _('Shows details of a AutoScalinig group')
    columns = ['ID', 'Name', 'instance_id', 'instance_name',
               'flavor_id', 'image_id', 'disk',
               'key_name', 'public_ip', 'user_data', 'metadata'
               ]

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            'config',
            metavar='<config>',
            help=_('ID or name of the configuration group')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        obj = client.find_config(parsed_args.config, ignore_missing=False)

        # display_columns, columns = _get_columns(obj)
        # data = utils.get_item_properties(
        #     obj, columns, formatters={'instance_config': _format_instance})

        fmt = set_attributes_for_print_detail(obj)
        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(
            fmt, self.columns, formatters={})

        return (self.columns, data)


class CreateAutoScalingConfig(command.ShowOne):
    _description = _('Creates AutoScalinig group')
    columns = ['ID', 'Name', 'instance_id', 'instance_name',
               'flavor_id', 'image_id', 'disk',
               'key_name', 'public_ip', 'user_data', 'metadata'
               ]

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('AS Configuration name')
        )
        group1 = parser.add_argument_group(
            'ECS', 'New scpecification template')
        group1.add_argument(
            '--flavor',
            metavar='<flavor>',
            help=_('Flavor ID or Name for the ECS instance')
        )
        group1.add_argument(
            '--image_id',
            metavar='<image_id>',
            help=_('Image ID for the ECS instance to be created')
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--instance_id',
            metavar='<instance_id>',
            help=_('AS Configuration name\n'
                   'Is mutually exclusive with ECS group')
        )

        parser.add_argument(
            '--disk',
            metavar='<disk>',
            action='append',
            help=_(
                'Disk information to attach to the instance.\n'
                'format = `DISK_TYPE`,`VOLUME_TYPE`,`SIZE`\n'
                '`DISK_TYPE` can be in [SYS, DATA] and identifies '
                'whether disk should be a system or data disk\n'
                '`VOLUME_TYPE` can be in: \n'
                '* `SATA` = Common I/O \n'
                '* `SAS` = High I/O \n'
                '* `SSD` = Ultra-High I/O \n'
                '`SIZE` is size in Gb\n'
                '(Repeat multiple times for multiple disks)')
        )

        parser.add_argument(
            '--key',
            metavar='<key>',
            help=_('Key name for the new ECS instance')
        )
        parser.add_argument(
            '--public_ip_bandwith',
            metavar='<public_ip_bandwith>',
            type=int,
            help=_('Defines EIP Bandwith (Mbit/s) to be attached '
                   'to the new ECS instance')
        )
        parser.add_argument(
            '--user_data',
            metavar='<user_data>',
            help=_('Path to the cloud-init user_data file')
        )
        parser.add_argument(
            '--metadata',
            metavar='<metadata>',
            help=_('User defined key=value pair '
                   'format KEY=VALUE '
                   'Cannot contain dot (`.`) or start with `$`')
        )
        return parser

    def take_action(self, parsed_args):

        config_attrs = {}
        if parsed_args.instance_id:
            config_attrs['instance_id'] = parsed_args.instance_id
        else:
            if not all(
                    [parsed_args.flavor,
                     parsed_args.image_id,
                     parsed_args.disk]):
                msg = _('Either instance_id or all of the '
                        '[flavor, image, disk] '
                        'should be given')
                raise argparse.ArgumentTypeError(msg)
            # config_attrs['name'] = parsed_args.name
            config_attrs['imageRef'] = parsed_args.image_id
            config_attrs['flavorRef'] = parsed_args.flavor
        config_attrs['key_name'] = parsed_args.key

        config_attrs['disk'] = []
        for disk in parsed_args.disk:
            disk_parts = disk.split(',')
            disk_data = {}
            if 3 == len(disk_parts):
                if disk_parts[0] in ('SYS', 'DATA'):
                    disk_data['disk_type'] = disk_parts[0]
                else:
                    msg = _('Disk Type is not in (SYS, DATA)')
                    raise argparse.ArgumentTypeError(msg)
                if disk_parts[1] in ('SATA', 'SAS', 'SSD'):
                    disk_data['volume_type'] = disk_parts[1]
                else:
                    msg = _('Volume Type is not in (SATA, SAS, SSD)')
                    raise argparse.ArgumentTypeError(msg)
                if disk_parts[2].isdigit:
                    disk_data['size'] = disk_parts[2]
                else:
                    msg = _('Volume SIZE is not a digit')
                    raise argparse.ArgumentTypeError(msg)
                config_attrs['disk'].append(disk_data)
            else:
                msg = _('Cannot parse disk information')
                raise argparse.ArgumentTypeError(msg)

        if parsed_args.public_ip_bandwith:
            ip_struct = {
                'eip': {
                    'ip_type': '5_bgp',
                    'bandwidth': {
                        'size': parsed_args.public_ip_bandwith,
                        'share_type': 'PER',
                        'charging_mode': 'traffic'
                    }
                }
            }
            config_attrs['public_ip'] = ip_struct

        if parsed_args.user_data:
            with open(parsed_args.user_data, 'r') as file:
                # Read the file (ASCII), encode Base64 and use that
                data = file.read().encode('ascii')
                data_b64 = base64.b64encode(data).decode('ascii')
                config_attrs['user_data'] = data_b64

        if parsed_args.metadata:
            config_attrs['metadata'] = {}
            k, v = parsed_args.metadata.split('=')
            config_attrs['metadata'][k] = v

        args = {}
        args['instance_config'] = config_attrs

        client = self.app.client_manager.auto_scaling

        instance = client.create_config(name=parsed_args.name, **args)

        fmt = set_attributes_for_print_detail(instance)
        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(
            fmt, self.columns, formatters={})

        return (self.columns, data)


class DeleteAutoScalingConfig(command.Command):
    _description = _('Deletes AutoScalinig group')

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            'config',
            nargs='+',
            metavar='<config>',
            help=_('AS Configuration ID')
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        # TODO(agoncharov) - proper error handling (reporting)

        if len(parsed_args.config) > 1:
            client.batch_delete_configs(parsed_args.config)
        elif len(parsed_args.config) == 1:
            client.delete_config(parsed_args.config[0], ignore_missing=False)
