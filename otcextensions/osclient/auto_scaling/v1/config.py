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
"""AS Configurations v1 action implementations"""

import argparse
import logging

import six

from osc_lib.command import command
from osc_lib.cli import format_columns
from osc_lib.cli import parseractions
from osc_lib import exceptions
from osc_lib import utils

from otcextensions.i18n import _

from otcextensions.osclient.auto_scaling import sdk_utils

LOG = logging.getLogger(__name__)


def _get_columns(item):
    column_map = {
        # 'instance_config:image_id': 'instance_config:image_id'
    }
    return sdk_utils.get_osc_show_columns_for_sdk_resource(item, column_map)


def _format_instance(inst):
    return inst.to_dict()


def set_attributes_for_print_detail(instance):
    info = {}  # instance._info.copy()
    info['name'] = instance.name
    info['id'] = instance.id
    info['create_time'] = instance.create_time
    instance_config = instance.instance_config
    # for (k,v) in six.iteritems(instance_config):
    #     info[k] = v
    if instance_config:
        info['instance_name'] = instance_config.instance_name
        info['instance_id'] = instance_config.instance_id
        info['flavor_id'] = instance_config.flavor_id
        info['image_id'] = instance_config.image_id
        info['key_name'] = instance_config.key_name
        info['public_ip'] = instance_config.public_ip
        info['user_data'] = instance_config.user_data
        info['disk'] = instance_config.disk
    # info['instance_config'] = format_columns.DictColumn(instance.instance_config),
    # info['flavor_id'] = instance.flavor['id']
    # if getattr(instance, 'volume', None):
    #     info['volume'] = instance.volume['size']
    #     if 'used' in instance.volume:
    #         info['volume_used'] = instance.volume['used']
    # if getattr(instance, 'ip', None):
    #     info['ip'] = ', '.join(instance.ip)
    # if getattr(instance, 'datastore', None):
    #     info['datastore'] = instance.datastore['type']
    #     info['datastore_version'] = instance.datastore['version']
    # if getattr(instance, 'configuration', None):
    #     info['configuration'] = instance.configuration['id']
    # if getattr(instance, 'replica_of', None):
    #     info['replica_of'] = instance.replica_of['id']
    # if getattr(instance, 'replicas', None):
    #     replicas = [replica['id'] for replica in instance.replicas]
    #     info['replicas'] = ', '.join(replicas)
    # if getattr(instance, 'networks', None):
    #     info['networks'] = instance.networks['name']
    #     info['networks_id'] = instance.networks['id']
    # if getattr(instance, 'fault', None):
    #     info.pop('fault', None)
    #     info['fault'] = instance.fault['message']
    #     info['fault_date'] = instance.fault['created']
    #     if 'details' in instance.fault and instance.fault['details']:
    #         info['fault_details'] = instance.fault['details']
    # info.pop('links', None)
    return info


class ListAutoScalingConfig(command.Lister):
    _description = _("List AutoScaling Configurations")
    columns = ('ID', 'Name')

    def get_parser(self, prog_name):
        parser = super(ListAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            '--limit',
            dest='limit',
            metavar='<limit>',
            type=int,
            default=None,
            help=_('Limit the number of results displayed. (Not supported)')
        )
        parser.add_argument(
            '--marker',
            dest='marker',
            metavar='<ID>',
            help=_('Begin displaying the results for IDs greater than the '
                   'specified marker. When used with --limit, set this to '
                   'the last ID displayed in the previous run. '
                   '(Not supported)')
        )

        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        data = client.configs()

        return (
            self.columns,
            (utils.get_item_properties(
                s,
                self.columns,
            ) for s in data)
        )


class ShowAutoScalingConfig(command.ShowOne):
    _description = _("Shows details of a AutoScalinig group")
    columns = ['ID', 'Name', 'Instance ID', 'Instance Name',
               'Flavor ID', 'Image ID', 'Disk',
               'Key Name', 'Public IP'
               ]

    def get_parser(self, prog_name):
        parser = super(ShowAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            'config',
            metavar="<config>",
            help=_("ID or name of the configuration group")
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
    _description = _("Creates AutoScalinig group")
    columns = ['ID', 'Name', 'Instance ID', 'Instance Name',
               'Flavor ID', 'Image ID', 'Disk',
               'Key Name', 'Public IP'
               ]

    def get_parser(self, prog_name):
        parser = super(CreateAutoScalingConfig, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar="<name>",
            help=_("AS Configuration name")
        )
        group1 = parser.add_argument_group('ECS', 'New scpecification template')
        group1.add_argument(
            '--flavor',
            metavar="<flavor>",
            help=_("Flavor ID or Name for the ECS instance")
        )
        group1.add_argument(
            '--image_id',
            metavar="<image_id>",
            help=_("Image ID for the ECS instance to be created")
        )
        group1.add_argument(
            '--disk',
            metavar="<disk>",
            action='append',
            help=_("Disk information to attach to the instance. \n"
                   "format = DISK_TYPE,VOLUME_TYPE,SIZE\n"
                   "'DISK_TYPE' can be in [SYS, DATA] and identifies "
                   "whether disk should be a system or data disk\n"
                   "'VOLUME_TYPE' can be in [SATA, SAS, SSD]\n"
                   "\t SATA = Common I/O\n"
                   "\t SAS = High I/O\n"
                   "\t SSD = Ultra-High I/O\n"
                   "'SIZE' is size in Gb\n"
                   "(Repeat multiple times for multiple disks)")
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--instance_id',
            metavar="<instance_id>",
            help=_("AS Configuration name\n"
                   "Is mutually exclusive with ECS group")
        )

        parser.add_argument(
            '--key',
            metavar="<key>",
            help=_("Key name for the new ECS instance")
        )
        parser.add_argument(
            '--public_ip',
            metavar="<public_ip>",
            help=_("Defines EIP Bandwith (Mbit/s) to be attached "
                   "to the new ECS instance")
        )
        return parser

    def take_action(self, parsed_args):
        client = self.app.client_manager.auto_scaling

        config_attrs = {}
        if parsed_args.instance_id:
            config_attrs['instance_id'] = parsed_args.instance_id
        else:
            if not all([parsed_args.flavor, parsed_args.image_id, parsed_args.disk]):
                msg = _("Either instance_id or all of the [flavor, image, disk] "
                        "should be given")
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
                        msg = _("Disk Type is not in (SYS, DATA)")
                        raise argparse.ArgumentTypeError(msg)
                    if disk_parts[1] in ('SATA', 'SAS', 'SSD'):
                        disk_data['volume_type'] = disk_parts[1]
                    else:
                        msg = _("Volume Type is not in (SATA, SAS, SSD)")
                        raise argparse.ArgumentTypeError(msg)
                    if disk_parts[2].isdigit:
                        disk_data['size'] = disk_parts[2]
                    else:
                        msg = _("Volume SIZE is not a digit")
                        raise argparse.ArgumentTypeError(msg)
                    config_attrs['disk'].append(disk_data)
                else:
                    msg = _("Cannot parse disk information")
                    raise argparse.ArgumentTypeError(msg)


        args = {}
        args['instance_config'] = config_attrs

        instance = client.create_config(name=parsed_args.name, **args)


        fmt = set_attributes_for_print_detail(instance)
        # display_columns, columns = _get_columns(obj)
        data = utils.get_dict_properties(
            fmt, self.columns, formatters={})

        return (self.columns, data)

        # return None
        # raise NotImplementedError


class DeleteAutoScalingConfig(command.ShowOne):
    _description = _("Deletes AutoScalinig group")
    columns = ['ID', 'Name', 'Status', 'Detail',
               'Datastore Version Name', 'Is Scaling']

    def get_parser(self, prog_name):
        parser = super(DeleteAutoScalingConfig, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        raise NotImplementedError
